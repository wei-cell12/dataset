#!/usr/bin/env python3
"""Generate unified Tier 1.2 manifest indexing Skill (12) + Memory (12) + Pure (12) = 36 items with SHA-256 audit."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path("/Users/zzh/Documents/Codex/2026-10-09/proofwriter50-users-zzh-documents-codex-2026")
D12 = ROOT / "dataset_1_2"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    modules = [
        ("skill", D12 / "skill_batch_12" / "benchmark_1_2_skill_12.json", D12 / "skill_batch_12"),
        ("memory", D12 / "memory_batch_12" / "benchmark_1_2_memory_12.json", D12 / "memory_batch_12"),
        ("pure", D12 / "pure_batch_12" / "benchmark_1_2_pure_12.json", D12 / "pure_batch_12"),
    ]
    d11_hashes = {
        sha256_file(p)
        for p in (ROOT / "dataset_1_1").rglob("*")
        if p.is_file() and p.suffix.lower() in {".png", ".jpg", ".jpeg"}
    }

    all_hashes: dict[str, str] = {}
    items = []
    domain_counts: dict[str, int] = {}
    regime_counts: dict[str, int] = {}

    for regime, jpath, base in modules:
        data = json.loads(jpath.read_text(encoding="utf-8"))
        regime_counts[regime] = len(data["cases"])
        for c in data["cases"]:
            img_p = base / c["source"]["image"]
            h = sha256_file(img_p)
            assert h not in d11_hashes, f"Overlap with dataset_1_1: {c['id']}"
            assert h not in all_hashes, f"Duplicate image inside Tier 1.2: {c['id']} vs {all_hashes[h]}"
            all_hashes[h] = c["id"]
            dom = c["domain"]
            domain_counts[dom] = domain_counts.get(dom, 0) + 1
            mode = c.get("skill_mode") or c.get("memory_mode") or c.get("pure_mode")
            items.append({
                "id": c["id"],
                "regime": regime,
                "domain": dom,
                "mode": mode,
                "image": str(img_p.relative_to(D12)),
                "dataset": c["source"]["dataset"],
                "sha256": h,
            })

    manifest = {
        "tier": "1.2",
        "total_items": len(items),
        "unique_images": len(all_hashes),
        "overlap_with_tier_1_1": 0,
        "by_regime": regime_counts,
        "by_domain": domain_counts,
        "bundles": {
            "skill": "skill_batch_12/benchmark_1_2_skill_12.json",
            "memory": "memory_batch_12/benchmark_1_2_memory_12.json",
            "pure": "pure_batch_12/benchmark_1_2_pure_12.json",
        },
        "items": items,
    }
    out = D12 / "tier_1_2_manifest.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out}: {len(items)} items, {len(all_hashes)} unique images, 0 overlap with 1.1.")
    print("by_regime:", regime_counts, "| by_domain:", domain_counts)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
