"""Live Evaluator for Tier 1.4 Multi-Step Compound-Misguidance Prototypes (`N` vs `M` arms).

Copies ONLY `workspace/` into a fresh opaque temp directory per episode (keeping `experiment/` completely
outside the sandbox), runs `agy` or `codex`, preserves raw output + SHA-256, and scores the 5 primary steps.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scoring.score_tier14 import score_tier14_output

AGY_BIN = "/Users/zzh/.local/bin/agy"
CODEX_BIN = "/opt/homebrew/bin/codex"


def _sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _extract_agy_final_text(stdout_text: str) -> str:
    """Reconstruct agent_response steps preserving step boundaries and guarding non-dict NDJSON lines."""
    steps: List[str] = []
    cur: List[str] = []
    for line in stdout_text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if not isinstance(obj, dict):
            continue
        su = obj.get("step_update")
        if not isinstance(su, dict):
            continue
        if su.get("step_type") == "agent_response":
            if su.get("text_delta"):
                cur.append(str(su["text_delta"]))
            if su.get("state") == "DONE" and cur:
                steps.append("".join(cur).strip())
                cur = []
    if cur:
        steps.append("".join(cur).strip())
    return "\n\n".join(s for s in steps if s).strip()


def _extract_codex_final_text(stdout_text: str) -> str:
    msgs: List[str] = []
    for line in stdout_text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if not isinstance(obj, dict):
            continue
        if obj.get("type") == "item.completed" and isinstance(obj.get("item"), dict):
            it = obj["item"]
            if it.get("type") == "agent_message" and it.get("text"):
                msgs.append(str(it["text"]))
    return "\n\n".join(msgs).strip()


def run_one_episode(
    task_dir: Path,
    arm: str,
    model: str,
    runner: str,
    timeout_s: int,
) -> Dict[str, Any]:
    task_id = task_dir.name
    exp_dir = task_dir / "experiment"
    prompt_text = (exp_dir / f"{arm}.txt").read_text(encoding="utf-8").strip()
    gold = json.loads((exp_dir / "gold.json").read_text(encoding="utf-8"))
    assertions_cfg = json.loads((exp_dir / "assertions.json").read_text(encoding="utf-8"))
    schema = json.loads((task_dir / "workspace/output.schema.json").read_text(encoding="utf-8"))

    full_prompt = (
        "You are operating inside a read-only audit workspace in your current working directory.\n"
        "Inspect all relevant files under `records/`, `policies/`, `communications/`, `images/`, and `output.schema.json` "
        "before answering. Return ONLY one valid JSON object matching `output.schema.json` as your final response.\n\n"
        f"{prompt_text}\n"
    )

    t0 = time.time()
    with tempfile.TemporaryDirectory(prefix="t14_sb_") as tmp:
        ws = Path(tmp) / "workspace"
        shutil.copytree(task_dir / "workspace", ws)
        if runner == "agy":
            cmd = [
                AGY_BIN,
                "--model",
                model,
                "--dangerously-skip-permissions",
                "--disable-slash-commands",
                "--output-format",
                "stream-json",
                "-p",
                full_prompt,
            ]
        else:
            cmd = [
                CODEX_BIN,
                "exec",
                "-m",
                model,
                "--sandbox",
                "read-only",
                "--skip-git-repo-check",
                "--json",
                "-C",
                str(ws),
                full_prompt,
            ]
        try:
            proc = subprocess.run(cmd, cwd=str(ws), capture_output=True, text=True, timeout=timeout_s)
            stdout_text = proc.stdout or ""
            stderr_text = proc.stderr or ""
            rc = proc.returncode
        except subprocess.TimeoutExpired as exc:
            raw_out = exc.stdout
            if isinstance(raw_out, bytes):
                stdout_text = raw_out.decode("utf-8", errors="replace")
            else:
                stdout_text = raw_out or ""
            stderr_text = f"TIMEOUT after {timeout_s}s"
            rc = -9

    elapsed = round(time.time() - t0, 2)
    final_text = _extract_agy_final_text(stdout_text) if runner == "agy" else _extract_codex_final_text(stdout_text)
    scored = score_tier14_output(final_text, gold, assertions_cfg, schema=schema)
    return {
        "task_id": task_id,
        "arm": arm,
        "model": model,
        "runner": runner,
        "returncode": rc,
        "elapsed_s": elapsed,
        "raw_stream_sha256": _sha256_text(stdout_text),
        "raw_response": final_text,
        "raw_response_sha256": _sha256_text(final_text),
        "stderr_tail": stderr_text[-500:] if stderr_text else "",
        **scored,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--runner", choices=["agy", "codex"], default="agy")
    ap.add_argument("--tag", default="pilot3")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--timeout", type=int, default=240)
    args = ap.parse_args()

    proto_root = ROOT / "prototypes"
    tasks = sorted(p for p in proto_root.iterdir() if p.is_dir() and (p / "experiment/gold.json").is_file())
    jobs = [(t, arm) for t in tasks for arm in ("N", "M")]

    results: List[Dict[str, Any]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = [ex.submit(run_one_episode, t, arm, args.model, args.runner, args.timeout) for t, arm in jobs]
        for fut in concurrent.futures.as_completed(futs):
            r = fut.result()
            results.append(r)
            bits = "".join("1" if b else "0" for b in r["five_bit"])
            traps = "".join("T" if b else "." for b in r["m_trap_hits"])
            print(f"[{r['task_id']} | {r['arm']}] rc={r['returncode']} scorable={r['scorable']} 5bit={bits} ({r['five_step_score']}/5) exact={r['full_object_exact']} traps={traps} ({r['elapsed_s']}s)", flush=True)

    results.sort(key=lambda x: (x["task_id"], x["arm"]))
    by_pair: Dict[str, Dict[str, Dict[str, Any]]] = {}
    for r in results:
        by_pair.setdefault(r["task_id"], {})[r["arm"]] = r

    step_names = ["scope", "policy", "image_A", "image_B", "final"]
    paired_flips = {s: [] for s in step_names}
    unresolved_by_arm = {"N": 0, "M": 0}
    resolved_pairs = 0
    for r in results:
        if not r["scorable"]:
            unresolved_by_arm[r["arm"]] += 1
    for tid, arms in sorted(by_pair.items()):
        if "N" in arms and "M" in arms and arms["N"]["scorable"] and arms["M"]["scorable"]:
            resolved_pairs += 1
            for i, s in enumerate(step_names):
                if arms["N"]["five_bit"][i] and not arms["M"]["five_bit"][i]:
                    paired_flips[s].append(tid)

    out_dir = ROOT / "eval_results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"eval_{args.model}_{args.tag}.json"
    summary = {
        "model": args.model,
        "runner": args.runner,
        "tag": args.tag,
        "total_episodes": len(results),
        "resolved_pairs": resolved_pairs,
        "unresolved_by_arm": unresolved_by_arm,
        "paired_n_pass_to_m_fail_by_step": paired_flips,
        "episodes": results,
    }
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nSaved: {out_path}")
    print("Paired N-pass -> M-fail flips by step:", paired_flips)


if __name__ == "__main__":
    main()
