"""Live Tier 1.3 Evaluator using `agy --output-format stream-json` inside opaque sandboxes.

Runs all 6 cells (U/V x N/A/Q) per family, translates native CLI tool events into
DeliveryEvents, grades each episode with `score_tier13.py`, and writes traces + report.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from broker.six_cell_renderer import render_all_six_cells
from schema.tier13_schema import sha256_file, sha256_text
from scoring.score_tier13 import score_episode, summarize_paired_family

AGY_BIN = "/Users/zzh/.local/bin/agy"
CODEX_BIN = "/opt/homebrew/bin/codex"
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def _parse_codex_stream(
    stdout_text: str,
    ws_root: Path,
    episode_id: str,
) -> Tuple[List[Dict[str, Any]], str, Dict[str, int], int]:
    """Translate `codex exec --json` NDJSON into DeliveryEvents + final text + token usage."""
    ws_resolved = ws_root.resolve()
    events: List[Dict[str, Any]] = []
    final_msgs: List[str] = []
    usage_totals = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
    step_num = 0
    all_files = [(str(p.relative_to(ws_resolved)), p) for p in ws_resolved.rglob("*") if p.is_file()]
    text_lines_cache: Dict[str, List[str]] = {}
    for rel, p in all_files:
        if p.suffix.lower() not in IMAGE_EXTS:
            text_lines_cache[rel] = p.read_text(encoding="utf-8", errors="replace").splitlines()

    for line in stdout_text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue

        etype = obj.get("type", "")
        if etype == "turn.completed" and isinstance(obj.get("usage"), dict):
            u = obj["usage"]
            inp = int(u.get("input_tokens") or 0)
            out = int(u.get("output_tokens") or 0)
            usage_totals["input_tokens"] += inp
            usage_totals["output_tokens"] += out
            usage_totals["total_tokens"] += inp + out
            continue

        if etype == "item.completed" and isinstance(obj.get("item"), dict):
            item = obj["item"]
            itype = item.get("type", "")
            if itype == "agent_message" and item.get("text"):
                final_msgs.append(str(item["text"]))
            elif itype in ("local_image", "image_view") or (
                itype == "tool_call" and str(item.get("name") or "").lower() in ("view_image", "read_image", "inspect_image")
            ):
                step_num += 1
                blob = json.dumps(item, ensure_ascii=False)
                for rel, p in all_files:
                    if p.suffix.lower() in IMAGE_EXTS and (rel in blob or p.name in blob):
                        ah = sha256_file(p)
                        events.append({
                            "episode_id": episode_id,
                            "step": step_num,
                            "tool": "view_image",
                            "rel_path": rel,
                            "asset_hash": ah,
                            "returned_locator": {"image": True},
                            "success": True,
                            "payload_hash": ah,
                            "truncated": False,
                            "error": None,
                        })
            elif itype == "command_execution":
                step_num += 1
                cmd = str(item.get("command") or "")
                out = str(item.get("aggregated_output") or item.get("output") or "")
                if not out.strip():
                    continue
                # Credit read_file ONLY when actual non-trivial content lines of a text file appear in command output.
                # Directory listings (ls/find/rg --files) emit zero file content lines and NEVER credit read_file or view_image.
                for rel, p in all_files:
                    if p.suffix.lower() in IMAGE_EXTS:
                        continue
                    file_lines = text_lines_cache.get(rel, [])
                    if not file_lines:
                        continue
                    matched_lns = [
                        ln_idx
                        for ln_idx, content_line in enumerate(file_lines, start=1)
                        if len(content_line.strip()) >= 12 and content_line.strip() in out
                    ]
                    if matched_lns:
                        ah = sha256_file(p)
                        total_lines = len(file_lines)
                        # Emit one event per CONTIGUOUS run of matched lines (prevents `head -1 && tail -1` gap spanning!)
                        runs: List[Tuple[int, int]] = []
                        r_start = r_end = matched_lns[0]
                        for ln_v in matched_lns[1:]:
                            if ln_v == r_end + 1:
                                r_end = ln_v
                            else:
                                runs.append((r_start, r_end))
                                r_start = r_end = ln_v
                        runs.append((r_start, r_end))
                        for rs, re_ln in runs:
                            events.append({
                                "episode_id": episode_id,
                                "step": step_num,
                                "tool": "read_file",
                                "rel_path": rel,
                                "asset_hash": ah,
                                "returned_locator": {
                                    "start_line": rs,
                                    "end_line": re_ln,
                                    "total_lines": total_lines,
                                    "eof_reached": re_ln >= total_lines,
                                },
                                "success": True,
                                "payload_hash": sha256_text(out[:2000]),
                                "truncated": False,
                                "error": None,
                            })

    return events, "\n".join(final_msgs).strip(), usage_totals, step_num


def _parse_agy_stream(
    stdout_text: str,
    ws_root: Path,
    episode_id: str,
) -> Tuple[List[Dict[str, Any]], str, Dict[str, int], int]:
    """Translate `agy --output-format stream-json` NDJSON into DeliveryEvents + final text + token usage."""
    ws_resolved = ws_root.resolve()
    events: List[Dict[str, Any]] = []
    final_chunks: List[str] = []
    usage_totals = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
    step_num = 0

    for line in stdout_text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue

        su = obj.get("step_update")
        if not isinstance(su, dict):
            continue

        if su.get("step_type") == "agent_response":
            if su.get("text_delta"):
                final_chunks.append(su["text_delta"])
            if su.get("state") == "DONE" and isinstance(su.get("usage"), dict):
                u = su["usage"]
                usage_totals["input_tokens"] += int(u.get("input_tokens") or 0)
                usage_totals["output_tokens"] += int(u.get("output_tokens") or 0)
                usage_totals["total_tokens"] += int(u.get("total_tokens") or 0)
            continue

        if su.get("step_type") == "tool" and su.get("state") == "DONE":
            step_num += 1
            tname = su.get("tool_name", "")
            tinfo = su.get("tool_info") or {}
            params = tinfo.get("parameters") or {}
            out_txt = str(tinfo.get("output") or "")

            if tname == "read_file":
                # Never credit failed / error read_file tool calls as delivered evidence!
                out_low = out_txt.strip().lower()
                if not out_low or out_low.startswith("error:") or "failed to read" in out_low or "no such file" in out_low or "permission denied" in out_low:
                    continue
                raw_path = str(params.get("Path") or "")
                p = ((ws_resolved / raw_path).resolve() if not Path(raw_path).is_absolute() else Path(raw_path).resolve()) if raw_path else None
                if p and p.is_file() and (ws_resolved in p.parents):
                    rel = str(p.relative_to(ws_resolved))
                    ah = sha256_file(p)
                    if p.suffix.lower() in IMAGE_EXTS:
                        events.append({
                            "episode_id": episode_id,
                            "step": step_num,
                            "tool": "view_image",
                            "rel_path": rel,
                            "asset_hash": ah,
                            "returned_locator": {"image": True},
                            "success": True,
                            "payload_hash": ah,
                            "truncated": False,
                            "error": None,
                        })
                    else:
                        # Credit ONLY actual contiguous content-line runs verified present in `out_txt`!
                        file_lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
                        total_lines = len(file_lines)
                        matched_lns = [
                            ln_idx
                            for ln_idx, content_line in enumerate(file_lines, start=1)
                            if len(content_line.strip()) >= 12 and content_line.strip() in out_txt
                        ]
                        if matched_lns:
                            runs: List[Tuple[int, int]] = []
                            r_start = r_end = matched_lns[0]
                            for ln_v in matched_lns[1:]:
                                if ln_v == r_end + 1:
                                    r_end = ln_v
                                else:
                                    runs.append((r_start, r_end))
                                    r_start = r_end = ln_v
                            runs.append((r_start, r_end))
                            for rs, re_ln in runs:
                                events.append({
                                    "episode_id": episode_id,
                                    "step": step_num,
                                    "tool": "read_file",
                                    "rel_path": rel,
                                    "asset_hash": ah,
                                    "returned_locator": {
                                        "start_line": rs,
                                        "end_line": re_ln,
                                        "total_lines": total_lines,
                                        "eof_reached": re_ln >= total_lines,
                                    },
                                    "success": True,
                                    "payload_hash": sha256_text(out_txt[:2000]),
                                    "truncated": re_ln < total_lines,
                                    "error": None,
                                })
            elif tname == "run_command":
                cmd = str(params.get("CommandLine") or "")
                if not out_txt.strip():
                    continue
                # Credit read_file ONLY for actual contiguous non-trivial content lines present in command output!
                for p in ws_resolved.rglob("*"):
                    if p.is_file() and p.suffix.lower() not in IMAGE_EXTS:
                        rel = str(p.relative_to(ws_resolved))
                        file_lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
                        if not file_lines:
                            continue
                        matched_lns = [
                            ln_idx
                            for ln_idx, content_line in enumerate(file_lines, start=1)
                            if len(content_line.strip()) >= 12 and content_line.strip() in out_txt
                        ]
                        if matched_lns:
                            ah = sha256_file(p)
                            total_lines = len(file_lines)
                            runs: List[Tuple[int, int]] = []
                            r_start = r_end = matched_lns[0]
                            for ln_v in matched_lns[1:]:
                                if ln_v == r_end + 1:
                                    r_end = ln_v
                                else:
                                    runs.append((r_start, r_end))
                                    r_start = r_end = ln_v
                            runs.append((r_start, r_end))
                            for rs, re_ln in runs:
                                events.append({
                                    "episode_id": episode_id,
                                    "step": step_num,
                                    "tool": "read_file",
                                    "rel_path": rel,
                                    "asset_hash": ah,
                                    "returned_locator": {
                                        "start_line": rs,
                                        "end_line": re_ln,
                                        "total_lines": total_lines,
                                        "eof_reached": re_ln >= total_lines,
                                    },
                                    "success": True,
                                    "payload_hash": sha256_text(out_txt[:2000]),
                                    "truncated": False,
                                    "error": None,
                                })

    return events, "".join(final_chunks).strip(), usage_totals, step_num


def run_one_cell(
    manifest: Dict[str, Any],
    cell: Dict[str, Any],
    model: str,
    runner: str = "agy",
    timeout: int = 180,
) -> Dict[str, Any]:
    episode_id = f"{cell['cell_id']}__{model}"
    t0 = time.time()

    with tempfile.TemporaryDirectory(prefix="ws_sb_") as td:
        ws = (Path(td) / "workspace").resolve()
        shutil.copytree(Path(cell["workspace_dir"]), ws)
        (ws / "deliverables").mkdir(parents=True, exist_ok=True)

        prompt = (
            "You are working inside the project workspace in your current working directory. "
            "Do NOT access any files outside this directory. Use your tools to inspect files and images "
            "as needed, then write the final JSON deliverable to the exact "
            f"relative path `{cell['deliverable_path']}`.\n\n"
            f"{cell['user_prompt']}"
        )

        infra_error = None
        stdout_text = ""
        stderr_text = ""
        cmd = (
            [
                CODEX_BIN,
                "exec",
                "-m", model,
                "--json",
                "--skip-git-repo-check",
                "-s", "workspace-write",
                "-C", str(ws),
                prompt,
            ]
            if runner == "codex"
            else [
                AGY_BIN,
                "--model", model,
                "--dangerously-skip-permissions",
                "--disable-slash-commands",
                "--output-format", "stream-json",
                "-p", prompt,
            ]
        )
        try:
            res = subprocess.run(
                cmd,
                cwd=str(ws),
                text=True,
                capture_output=True,
                timeout=timeout,
            )
            stdout_text = res.stdout or ""
            stderr_text = res.stderr or ""
            if "RESOURCE_EXHAUSTED" in stderr_text or "quota reached" in stderr_text.lower() or "RESOURCE_EXHAUSTED" in stdout_text:
                infra_error = "QUOTA_EXHAUSTED"
        except subprocess.TimeoutExpired:
            infra_error = "TIMEOUT"

        elapsed = round(time.time() - t0, 2)
        if runner == "codex":
            events, final_chat, usage_totals, steps_used = _parse_codex_stream(stdout_text, ws, episode_id)
        else:
            events, final_chat, usage_totals, steps_used = _parse_agy_stream(stdout_text, ws, episode_id)

        deliv_file = ws / cell["deliverable_path"]
        submitted_path = None
        submitted_content = None
        submitted_hash = None
        term_reason = "infra_error" if infra_error else "no_file_written"

        if deliv_file.is_file():
            submitted_path = cell["deliverable_path"]
            submitted_content = deliv_file.read_text(encoding="utf-8", errors="replace")
            submitted_hash = sha256_text(submitted_content)
            term_reason = "submitted"

        trace = {
            "episode_id": episode_id,
            "model": model,
            "steps_used": steps_used,
            "elapsed_sec": elapsed,
            "usage": usage_totals,
            "infra_error": infra_error,
            "termination_reason": term_reason,
            "submitted_path": submitted_path,
            "submitted_hash": submitted_hash,
            "submitted_content": submitted_content,
            "final_chat_preview": final_chat[:500],
            "events": events,
        }

    scored = score_episode(manifest, cell["evidence_state"], cell["guidance_direction"], trace)
    scored["model"] = model
    scored["elapsed_sec"] = elapsed
    scored["usage"] = usage_totals
    scored["infra_error"] = infra_error
    scored["submitted_content"] = submitted_content
    scored["images_viewed"] = sorted({e["rel_path"] for e in events if e["tool"] == "view_image" and e["success"]})
    scored["files_read_count"] = len({e["rel_path"] for e in events if e["tool"] == "read_file" and e["success"]})
    return {"trace": trace, "scored": scored}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="gemini-3.8-flash-low")
    ap.add_argument("--runner", choices=["agy", "codex"], default="agy")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--tag", default="phase0")
    ap.add_argument("--families-dir", default="families")
    ap.add_argument("--families", nargs="*", default=None)
    args = ap.parse_args()

    fam_root = ROOT / args.families_dir
    fam_dirs = sorted(p for p in fam_root.iterdir() if p.is_dir() and (p / "manifest.json").is_file())
    if args.families:
        fam_dirs = [p for p in fam_dirs if p.name in args.families]

    jobs = []
    manifests: Dict[str, Dict[str, Any]] = {}
    for fdir in fam_dirs:
        m = json.loads((fdir / "manifest.json").read_text(encoding="utf-8"))
        manifests[m["family_id"]] = m
        for cell in render_all_six_cells(m, fdir):
            jobs.append((m, cell))

    out_dir = ROOT / "eval_results"
    out_dir.mkdir(parents=True, exist_ok=True)
    safe_model = args.model.replace("/", "_")
    out_json = out_dir / f"eval_{safe_model}_{args.tag}.json"
    out_jsonl = out_dir / f"eval_{safe_model}_{args.tag}.jsonl"

    # Load resumable completed episodes (skip infra_error so failed ones auto-retry!)
    completed_by_id: Dict[str, Dict[str, Any]] = {}
    if out_jsonl.is_file():
        for line in out_jsonl.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                rec = json.loads(line)
                sc = rec.get("scored", {})
                ep_id = sc.get("episode_id")
                if ep_id and not sc.get("infra_error") and sc.get("scorable_final"):
                    completed_by_id[ep_id] = rec
            except Exception:
                continue

    pending_jobs = [
        (m, c) for m, c in jobs if f"{c['cell_id']}__{args.model}" not in completed_by_id
    ]
    print(
        f"Running {len(pending_jobs)} pending / {len(jobs)} total episodes on "
        f"model={args.model} runner={args.runner} (workers={args.workers}, resumed={len(completed_by_id)})...",
        flush=True,
    )

    import threading
    write_lock = threading.Lock()
    results: List[Dict[str, Any]] = list(completed_by_id.values())

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(run_one_cell, m, c, args.model, args.runner, args.timeout) for m, c in pending_jobs]
        for fut in concurrent.futures.as_completed(futs):
            r = fut.result()
            sc = r["scored"]
            results.append(r)
            with write_lock:
                with out_jsonl.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            print(
                f"  [{len(results)}/{len(jobs)}] [{sc['family_id']} | {sc['evidence_state']}/{sc['guidance_direction']} ({sc['guidance_alignment'][:4]})] "
                f"focal_pass={sc['focal_pass']} whole={sc['whole_deliverable_pass']} "
                f"E={sc['focal_evidence_delivered']} wrong_steer={sc['adopted_wrong_steer']} "
                f"err={sc['error_class']} imgs={len(sc['images_viewed'])} steps={sc['steps_used']} ({sc['elapsed_sec']}s)",
                flush=True,
            )

    # Deduplicate by episode_id keeping latest
    dedup: Dict[str, Dict[str, Any]] = {}
    for r in results:
        dedup[r["scored"]["episode_id"]] = r
    results = sorted(
        dedup.values(),
        key=lambda r: (r["scored"]["family_id"], r["scored"]["evidence_state"], r["scored"]["guidance_direction"]),
    )

    by_fam: Dict[str, List[Dict[str, Any]]] = {}
    for r in results:
        by_fam.setdefault(r["scored"]["family_id"], []).append(r["scored"])

    paired_summaries = {fid: summarize_paired_family(rows) for fid, rows in by_fam.items()}
    payload = {
        "model": args.model,
        "total_episodes": len(results),
        "paired_summaries": paired_summaries,
        "scored_rows": [r["scored"] for r in results],
        "traces": [r["trace"] for r in results],
    }
    out_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nSaved full results -> {out_json}", flush=True)
    # Compact aggregate headline
    sc_rows = payload["scored_rows"]
    usable = [r for r in sc_rows if not r.get("infra_error") and r.get("scorable_final")]
    n_rows = [r for r in usable if r["guidance_direction"] == "N"]
    ua_rows = [r for r in usable if r["evidence_state"] == "U" and r["guidance_direction"] == "A"]
    vq_rows = [r for r in usable if r["evidence_state"] == "V" and r["guidance_direction"] == "Q"]
    good_rows = [r for r in usable if r["guidance_alignment"] == "boundary_keeping"]
    print(
        f"\n=== HEADLINE ({args.model}, usable={len(usable)}/{len(sc_rows)}) ===\n"
        f"  N (No Guidance) focal pass : {sum(r['focal_pass'] for r in n_rows)}/{len(n_rows)}\n"
        f"  Correct Guidance focal pass: {sum(r['focal_pass'] for r in good_rows)}/{len(good_rows)}\n"
        f"  U/A Wrong-Steer Flip       : {sum(r['adopted_wrong_steer'] for r in ua_rows)}/{len(ua_rows)}\n"
        f"  V/Q Wrong-Steer Flip       : {sum(r['adopted_wrong_steer'] for r in vq_rows)}/{len(vq_rows)}",
        flush=True,
    )


if __name__ == "__main__":
    main()
