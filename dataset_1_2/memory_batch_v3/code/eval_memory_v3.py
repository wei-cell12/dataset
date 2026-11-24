#!/usr/bin/env python3
"""Evaluator for memory_batch_v3 using agy (Gemini 3.8 Flash etc.) across M0, M_mem, M_syco."""

from __future__ import annotations

import concurrent.futures
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

MV3 = Path("/Users/zzh/Documents/Codex/2026-10-09/proofwriter50-users-zzh-documents-codex-2026/dataset_1_2/memory_batch_v3")
DATA = json.loads((MV3 / "benchmark_1_2_memory_v3.json").read_text(encoding="utf-8"))
AGY = "/Users/zzh/.local/bin/agy"


def call_agy(model: str, img_path: Path, prompt: str, sb: Path) -> tuple[str, float]:
    local_img = sb / f"attached_image{img_path.suffix}"
    shutil.copy2(img_path, local_img)
    full_prompt = (
        f"First inspect the attached image file at `{local_img}` using your file-reading tool. "
        "Do not access any files outside this directory. Then answer the user directly.\n\n"
        f"{prompt}"
    )
    for _ in range(2):
        t0 = time.time()
        try:
            res = subprocess.run(
                [
                    AGY, "--model", model,
                    "--dangerously-skip-permissions",
                    "--disable-slash-commands",
                    "-p", full_prompt,
                ],
                cwd=str(sb), text=True, capture_output=True, timeout=120,
            )
            txt = (res.stdout or "").strip()
            if txt:
                return txt, round(time.time() - t0, 1)
        except subprocess.TimeoutExpired:
            continue
    return "<TIMEOUT>", 120.0


def build_prompt(case: dict, cond: str) -> str:
    cobj = case["conditions"][cond]
    user_prompt = cobj["user_prompt"]
    if not cobj["include_memory"]:
        return user_prompt

    mem_lines = "\n".join(
        f"- [{m['date']} | {m['category']}] {m['content']}" for m in case["retrieved_memory"]
    )
    dlg_lines = "\n".join(
        f"- ({d['session']}) {d['role'].capitalize()}: {d['content']}" for d in case["past_dialogue"]
    )
    return (
        f"[Retrieved User Memory]\n{mem_lines}\n\n"
        f"[Relevant Past Conversation Excerpts]\n{dlg_lines}\n\n"
        f"[Current Turn]\nUser: {user_prompt}"
    )


def main() -> int:
    model = sys.argv[1] if len(sys.argv) > 1 else "gemini-3.8-flash-low"
    conds = sys.argv[2].split(",") if len(sys.argv) > 2 else ["M0", "M_mem", "M_syco"]
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 4

    def run_one(case: dict, cond: str) -> dict:
        cid = case["id"]
        img_path = MV3 / case["source"]["image"]
        prompt = build_prompt(case, cond)
        with tempfile.TemporaryDirectory(prefix=f"mv3_{cid}_{cond}_") as tmp:
            sb = Path(tmp)
            resp, sec = call_agy(model, img_path, prompt, sb)
        return {
            "id": cid,
            "domain": case["domain"],
            "memory_mode": case["memory_mode"],
            "condition": cond,
            "model": model,
            "sec": sec,
            "response": resp,
        }

    tasks = [(c, cond) for c in DATA["cases"] for cond in conds]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        futs = [pool.submit(run_one, *t) for t in tasks]
        for f in concurrent.futures.as_completed(futs):
            r = f.result()
            results.append(r)
            snip = r["response"].replace("\n", " ")[:120]
            print(f"[{model} | {r['id']} ({r['memory_mode'][:8]}) | {r['condition']}] {r['sec']}s | {snip}", flush=True)

    results.sort(key=lambda r: (r["id"], conds.index(r["condition"])))
    out_dir = MV3 / "eval_results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_p = out_dir / f"eval_{model}_{'_'.join(conds)}.json"
    out_p.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {out_p} ({len(results)} runs).", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
