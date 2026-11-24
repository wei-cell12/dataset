#!/usr/bin/env python3
"""Download fresh deduplicated candidate images for Tier 1.2 scale-up (120 -> 240 items)."""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path("/Users/zzh/Documents/Codex/2026-10-09/proofwriter50-users-zzh-documents-codex-2026")
D12 = ROOT / "dataset_1_2"
POOL = D12 / "scale_240" / "candidate_pool"


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def collect_existing_hashes() -> set[str]:
    hashes = set()
    for base in [
        ROOT / "dataset_1_1" / "images",
        D12 / "skill_40" / "images",
        D12 / "memory_40" / "images",
        D12 / "pure_40" / "images",
        D12 / "scale_120" / "candidate_pool",
    ]:
        if base.exists():
            for f in base.rglob("*"):
                if f.is_file() and f.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
                    hashes.add(sha256_bytes(f.read_bytes()))
    return hashes


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_bytes(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def extract_img_info(row: dict) -> tuple[str | None, str]:
    for key in ("image", "image_1"):
        val = row.get(key)
        if isinstance(val, dict) and val.get("src"):
            src = val["src"]
            ext = ".png"
            low = src.lower()
            if ".jpg" in low or ".jpeg" in low:
                ext = ".jpg"
            return src, ext
    return None, ".png"


SPECS = [
    # Chart_data
    ("chartqa_p2", "HuggingFaceM4/ChartQA", "default", "test", 70, 45),
    ("charxiv_p2", "princeton-nlp/CharXiv", "default", "validation", 60, 30),
    # Medical (objective biostats/epi tables & imaging QA)
    ("mmmu_ph_p2", "MMMU/MMMU", "Public_Health", "test", 0, 45),
    ("vqarad_p2", "flaviagiammarino/vqa-rad", "default", "test", 60, 35),
    # Daily_life (receipts, accounting/finance tables, everyday photos)
    ("mmmu_acct_p2", "MMMU/MMMU", "Accounting", "test", 0, 25),
    ("mmmu_fin_p2", "MMMU/MMMU", "Finance", "test", 0, 25),
    ("cord_p2", "naver-clova-ix/cord-v2", "default", "test", 0, 20),
    ("rwqa_p2", "visheratin/realworldqa", "default", "test", 90, 25),
]


def download_spec(spec: tuple[str, str, str, str, int, int], used_hashes: set[str]) -> list[dict]:
    folder, dataset, config, split, offset, length = spec
    out_dir = POOL / folder
    out_dir.mkdir(parents=True, exist_ok=True)
    qs = urllib.parse.urlencode({
        "dataset": dataset, "config": config, "split": split,
        "offset": offset, "length": length,
    })
    url = f"https://datasets-server.huggingface.co/rows?{qs}"
    try:
        data = fetch_json(url)
    except Exception as e:
        print(f"[ERR] {folder}: {e}", flush=True)
        return []

    records = []
    local_hashes = set()
    for item in data.get("rows", []):
        ridx = item["row_idx"]
        row = item["row"]
        src, ext = extract_img_info(row)
        if not src:
            continue
        try:
            raw = fetch_bytes(src)
        except Exception:
            continue
        if len(raw) < 2000:
            continue
        h = sha256_bytes(raw)
        if h in used_hashes or h in local_hashes:
            continue
        local_hashes.add(h)
        fname = f"{folder}_{ridx:03d}{ext}"
        fpath = out_dir / fname
        fpath.write_bytes(raw)
        meta = {}
        for k in ("question", "query", "reasoning_q", "descriptive_q"):
            if row.get(k):
                meta[k] = str(row[k])[:160]
        records.append({
            "folder": folder,
            "file": f"{folder}/{fname}",
            "dataset": dataset,
            "config": config,
            "split": split,
            "row_idx": ridx,
            "sha256": h,
            "bytes": len(raw),
            "meta": meta,
        })
    print(f"[OK] {folder}: downloaded {len(records)} fresh unique images", flush=True)
    return records


def main() -> int:
    POOL.mkdir(parents=True, exist_ok=True)
    used_hashes = collect_existing_hashes()
    print(f"Loaded {len(used_hashes)} existing image hashes to exclude.", flush=True)
    all_records = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        futs = [ex.submit(download_spec, sp, used_hashes) for sp in SPECS]
        for f in concurrent.futures.as_completed(futs):
            all_records.extend(f.result())
    # Deduplicate across folders
    dedup = []
    seen = set()
    for r in sorted(all_records, key=lambda x: x["file"]):
        if r["sha256"] in seen:
            (POOL / r["file"]).unlink(missing_ok=True)
            continue
        seen.add(r["sha256"])
        dedup.append(r)
    (POOL / "pool_index_240.json").write_text(json.dumps(dedup, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"TOTAL fresh unique images in scale_240/candidate_pool: {len(dedup)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
