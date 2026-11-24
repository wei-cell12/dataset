#!/usr/bin/env python3
"""Run truly independent, single-turn ephemeral GPT evaluations on Tier 1.2 Pilot."""

import concurrent.futures
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

D1_2 = Path("/Users/zzh/Documents/Codex/2026-10-09/proofwriter50-users-zzh-documents-codex-2026/dataset_1_2")
PILOT_PATH = D1_2 / "pilot_1_2.json"
OUT_DIR = D1_2 / "eval_pilot_results"
CODEX_BIN = "/opt/homebrew/bin/codex"


def run_one(item: dict, condition: str, model: str, effort: str, sandbox_dir: Path) -> dict:
    uid = item["unit_id"]
    img_path = str(D1_2 / item["image_path"])
    prompt = item["variants"][condition]["prompt"]
    out_file = sandbox_dir / f"{uid}__{condition}.txt"

    cmd = [
        CODEX_BIN,
        "exec",
        "--ephemeral",
        "--skip-git-repo-check",
        "-s",
        "read-only",
        "-C",
        str(sandbox_dir),
        "-m",
        model,
        "-c",
        f'model_reasoning_effort="{effort}"',
        "-i",
        img_path,
        "-o",
        str(out_file),
        "-",
    ]
    t0 = time.time()
    proc = subprocess.run(
        cmd,
        input=prompt,
        text=True,
        capture_output=True,
        timeout=180,
    )
    elapsed = round(time.time() - t0, 2)
    response = out_file.read_text(encoding="utf-8").strip() if out_file.exists() else ""
    return {
        "unit_id": uid,
        "domain": item["domain"],
        "fallacy_type": item["fallacy_type"],
        "context_conflict_type": item["context_conflict_type"],
        "pressure_type": item["variants"]["syco_pressure"]["pressure_type"] if condition == "syco_pressure" else None,
        "condition": condition,
        "model": model,
        "effort": effort,
        "returncode": proc.returncode,
        "elapsed_sec": elapsed,
        "prompt": prompt,
        "response": response,
        "stderr_tail": proc.stderr[-300:] if proc.returncode != 0 else "",
    }


def main() -> int:
    model = sys.argv[1] if len(sys.argv) > 1 else "gpt-6.1-sol"
    effort = sys.argv[2] if len(sys.argv) > 2 else "low"
    conditions = sys.argv[3].split(",") if len(sys.argv) > 3 else ["neutral", "syco_pressure"]
    max_workers = int(sys.argv[4]) if len(sys.argv) > 4 else 5

    items = json.loads(PILOT_PATH.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []

    with tempfile.TemporaryDirectory(prefix="codex_blind_eval_") as tmp:
        sandbox_dir = Path(tmp)
        tasks = [(item, cond) for item in items for cond in conditions]
        print(f"Launching {len(tasks)} independent ephemeral calls: model={model}, effort={effort}, workers={max_workers}", flush=True)

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
            futs = {
                pool.submit(run_one, item, cond, model, effort, sandbox_dir): (item["unit_id"], cond)
                for item, cond in tasks
            }
            done = 0
            for fut in concurrent.futures.as_completed(futs):
                uid, cond = futs[fut]
                res = fut.result()
                results.append(res)
                done += 1
                preview = res["response"].replace("\n", " ")[:90]
                print(f"[{done}/{len(tasks)}] {uid} ({cond}) rc={res['returncode']} {res['elapsed_sec']}s | {preview}", flush=True)

    # Sort deterministically by unit_id then condition
    order = {it["unit_id"]: i for i, it in enumerate(items)}
    results.sort(key=lambda r: (order.get(r["unit_id"], 999), conditions.index(r["condition"])))

    out_json = OUT_DIR / f"pilot_eval_{model}_{effort}.json"
    out_json.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {len(results)} results to {out_json}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
