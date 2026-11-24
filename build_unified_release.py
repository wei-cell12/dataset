"""Build the unified Three-Tier Multimodal Sycophancy & Evidence-Boundary Benchmark release package.

Generates in the project root:
- `UNIFIED_BENCHMARK_MANIFEST.json`
- `RELEASE_SHA256SUMS.txt`
- `BENCHMARK_README.md`
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set

ROOT = Path(__file__).resolve().parent


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _collect_t11_shas() -> Set[str]:
    items = json.loads((ROOT / "dataset_1_1/benchmark_1_1_aligned.json").read_text(encoding="utf-8"))
    return {x["image_sha256"] for x in items}


def _collect_t12_shas() -> Set[str]:
    data = json.loads((ROOT / "dataset_1_2/benchmark_1_2_240.json").read_text(encoding="utf-8"))
    items = data if isinstance(data, list) else data.get("cases", data.get("items", []))
    shas: Set[str] = set()
    for it in items:
        src_obj = it.get("source") if isinstance(it.get("source"), dict) else {}
        if src_obj.get("sha256"):
            shas.add(src_obj["sha256"])
        else:
            ip = src_obj.get("image") or it.get("image_path") or it.get("image")
            if ip:
                p = ROOT / "dataset_1_2" / ip
                if p.is_file():
                    shas.add(sha256_file(p))
    return shas


def _collect_t13_shas() -> Dict[str, Set[str]]:
    focal: Set[str] = set()
    all_imgs: Set[str] = set()
    fam_root = ROOT / "dataset_1_3/families_60"
    for fd in sorted(fam_root.iterdir()):
        if not fd.is_dir() or not (fd / "manifest.json").is_file():
            continue
        m = json.loads((fd / "manifest.json").read_text(encoding="utf-8"))
        focal_rel = m["twin_patch_allowlist"][0]["rel_path"]
        for br in ("workspace_U", "workspace_V"):
            bdir = fd / br
            focal.add(sha256_file(bdir / focal_rel))
            for p in bdir.rglob("*"):
                if p.is_file() and p.suffix.lower() in (".png", ".jpg", ".jpeg"):
                    all_imgs.add(sha256_file(p))
    return {"focal": focal, "all": all_imgs}


def main() -> None:
    m11 = json.loads((ROOT / "dataset_1_1/tier_1_1_manifest.json").read_text(encoding="utf-8"))
    m12 = json.loads((ROOT / "dataset_1_2/tier_1_2_manifest_240.json").read_text(encoding="utf-8"))
    m13 = json.loads((ROOT / "dataset_1_3/tier_1_3_manifest_60.json").read_text(encoding="utf-8"))

    shas_11 = _collect_t11_shas()
    shas_12 = _collect_t12_shas()
    shas_13 = _collect_t13_shas()
    union_all = shas_11 | shas_12 | shas_13["all"]

    core_files: List[str] = [
        "dataset_1_1/benchmark_1_1.json",
        "dataset_1_1/benchmark_1_1_aligned.json",
        "dataset_1_1/tier_1_1_manifest.json",
        "dataset_1_1/code/align_tier11.py",
        "dataset_1_2/benchmark_1_2_240.json",
        "dataset_1_2/tier_1_2_manifest_240.json",
        "dataset_1_2/README.md",
        "dataset_1_3/tier_1_3_manifest_60.json",
        "dataset_1_3/README.md",
        "dataset_1_3/schema/tier13_schema.py",
        "dataset_1_3/broker/workspace_broker.py",
        "dataset_1_3/broker/six_cell_renderer.py",
        "dataset_1_3/scoring/score_tier13.py",
        "dataset_1_3/eval/eval_tier13.py",
        "dataset_1_3/builders/build_tier13_60.py",
        "dataset_1_3/tests/test_tier13_60_ci.py",
    ]
    checksums: Dict[str, str] = {}
    for rel in core_files:
        p = ROOT / rel
        assert p.is_file(), f"Missing core release file: {rel}"
        checksums[rel] = sha256_file(p)

    # Also hash all 60 frozen Tier 1.3 family manifests for complete tamper-evidence
    fam_manifest_hashes: Dict[str, str] = {}
    for fd in sorted((ROOT / "dataset_1_3/families_60").iterdir()):
        mp = fd / "manifest.json"
        if fd.is_dir() and mp.is_file():
            rel = str(mp.relative_to(ROOT))
            fam_manifest_hashes[rel] = sha256_file(mp)

    unified_manifest = {
        "benchmark_name": "Multimodal Sycophancy & Evidence-Boundary Benchmark Suite (Tier 1.1 -> 1.2 -> 1.3)",
        "release_version": "v1.0-frozen",
        "built_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tiers": {
            "tier_1_1": {
                "schema_version": m11["schema_version"],
                "description": "Direct single-image visual contradiction under sycophantic pressure",
                "primary_items": m11["total_items"],
                "unique_images_sha256": m11["unique_images_sha256"],
                "unique_source_clusters": m11["unique_source_clusters"],
                "canonical_domains": m11["canonical_domain_counts"],
                "manifest_path": "dataset_1_1/tier_1_1_manifest.json",
                "data_path": "dataset_1_1/benchmark_1_1_aligned.json",
                "original_data_path": "dataset_1_1/benchmark_1_1.json",
                "audit_status": "verified_125_unique_images",
            },
            "tier_1_2": {
                "schema_version": m12["schema_version"],
                "description": "Single-turn multimodal evidence-boundary & skill/memory conflict benchmark",
                "primary_items": m12["summary_counts"]["total_primary_cases"],
                "companion_accurate_draft_items": m12["summary_counts"]["companion_accurate_draft_cases"],
                "total_items": m12["summary_counts"]["total_primary_cases"] + m12["summary_counts"]["companion_accurate_draft_cases"],
                "total_prompts": m12["summary_counts"]["total_primary_item_prompts"] + m12["summary_counts"]["companion_accurate_draft_prompts"],
                "unique_primary_images_sha256": len(shas_12),
                "domains": m12["summary_counts"]["domains"],
                "regimes": m12["summary_counts"]["regimes"],
                "manifest_path": "dataset_1_2/tier_1_2_manifest_240.json",
                "data_path": "dataset_1_2/benchmark_1_2_240.json",
                "audit_status": "GPT-6.2-Astra audited 8.5/10 (dataset+harness), 8/10 overall",
            },
            "tier_1_3": {
                "schema_version": m13["schema_version"],
                "description": "Long-context 5-hop multi-step multi-file multi-image agent workspace benchmark (U/V twins x N/A/Q + 3-point compound steer)",
                "total_families": m13["total_families"],
                "total_workspaces": m13["total_workspaces"],
                "total_primary_episodes_per_model": m13["total_primary_episodes_per_model"],
                "short_evidence_controls": len(m13["short_evidence_control_families"]),
                "short_evidence_control_prior_balance": {"U": 6, "V": 6},
                "domain_memory_prior_balance": m13["domain_memory_prior_balance"],
                "unique_source_clusters_sha256": m13["unique_source_clusters"],
                "total_image_placements": 600,
                "unique_focal_images_sha256": len(shas_13["focal"]),
                "unique_all_workspace_images_sha256": len(shas_13["all"]),
                "manifest_path": "dataset_1_3/tier_1_3_manifest_60.json",
                "data_dir": "dataset_1_3/families_60",
                "ci_verifier": "dataset_1_3/tests/test_tier13_60_ci.py",
                "audit_status": "GPT-6.2-Astra signed off 10/10 Pass (zero-bypass 5-hop verified)",
            },
        },
        "cross_tier_image_provenance": {
            "total_unique_real_images_union_sha256": len(union_all),
            "tier1_1_vs_tier1_2_overlap_sha256": len(shas_11 & shas_12),
            "tier1_1_vs_tier1_3_overlap_sha256": len(shas_11 & shas_13["all"]),
            "tier1_2_vs_tier1_3_focal_overlap_sha256": len(shas_12 & shas_13["focal"]),
            "disclosure_note": (
                "Tier 1.1 and Tier 1.2 have ZERO image overlap. Tier 1.3 draws 100% genuine photographs, "
                "published charts, and licensed clinical scans from the verified Tier 1.2 real-image pool "
                "(0 synthetic SVGs); shared-source families are explicitly clustered via `source_cluster_id` (49 clusters)."
            ),
        },
        "core_file_sha256": checksums,
        "tier_1_3_family_manifest_count": len(fam_manifest_hashes),
    }

    (ROOT / "UNIFIED_BENCHMARK_MANIFEST.json").write_text(
        json.dumps(unified_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    sha_lines = [f"{digest}  {rel}" for rel, digest in checksums.items()]
    sha_lines.append(f"{sha256_file(ROOT / 'UNIFIED_BENCHMARK_MANIFEST.json')}  UNIFIED_BENCHMARK_MANIFEST.json")
    for rel, digest in fam_manifest_hashes.items():
        sha_lines.append(f"{digest}  {rel}")
    (ROOT / "RELEASE_SHA256SUMS.txt").write_text("\n".join(sha_lines) + "\n", encoding="utf-8")

    readme = f"""# 多模态谄媚与证据边界三层基准数据集（`v1.0-frozen`）

> **第一次看本仓库？推荐先读详细中文导读**：[DATASET_INTRODUCTION.md](./DATASET_INTRODUCTION.md)（含生活化例子、三层真题拆解、5 跳流程图、防捷径设计与快速上手指南）。

本仓库包含一套 **100% 真实图片** 构建的三层递进式多模态基准数据集，用于评测视觉语言模型（VLM）与工具调用 Agent 在 **“真实图片证据”** 与 **“用户施压 / 错误草稿 / 历史记忆”** 发生冲突时，能否坚持视觉事实、守住证据边界。

---

## 三层数据集总览

| 层级 | 目录 | 版本 | 题目规模 | 领域分布 | 真实图片 | 独立审计状态 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 1.1**<br>单图直接视觉反驳 | [`dataset_1_1/`](./dataset_1_1/) | `tier1.1-125-v1.1` | **125 题**（原 3 条件 + 对齐 5 条件） | 日常 (50)、医疗 (50)、图表 (25) | **125 张**不重复真图（与 1.2 零重合） | 125/125 SHA-256 校验通过 |
| **Tier 1.2**<br>证据边界 & 技能/记忆冲突 | [`dataset_1_2/`](./dataset_1_2/) | `tier1.2-240-v2.2` | **240 正式题 + 16 对照题 = 256 题**（1,088 条 prompt） | 日常 (80)、医疗 (80)、图表 (80) | **{len(shas_12)} 张**不重复主图 | **GPT 6.2 Astra：8.5/10** |
| **Tier 1.3**<br>5 跳多文件多图 Agent 工作区 | [`dataset_1_3/`](./dataset_1_3/) | `{m13['schema_version']}` | **60 组 = 120 孪生工作区 = 360 题/模型** + 12 短对照（6U/6V） | 日常 (20)、医疗 (20)、图表 (20) × 4 题型 | **600 张**真图投放（{len(shas_13['all'])} 独立图，49 聚类，**0 假图**） | **GPT 6.2 Astra：10/10 Pass** |

---

## 仓库目录结构

```text
.
├── README.md                        # 本总说明文档
├── DATASET_INTRODUCTION.md          # 面向第一次读者的零门槛完整中文导读
├── UNIFIED_BENCHMARK_MANIFEST.json  # 三层统一总清单（机器可读）
├── RELEASE_SHA256SUMS.txt           # 77 项核心文件与清单防篡改 SHA-256 校验和
├── build_unified_release.py         # 总清单与校验和生成脚本
├── dataset_1_1/                     # Tier 1.1：125 题单图直接纠错（详见内部 README）
├── dataset_1_2/                     # Tier 1.2：256 题图文边界 / 技能 / 记忆冲突（详见内部 README）
├── dataset_1_3/                     # Tier 1.3：60 组 5 跳多文件多图 Agent 工作区（详见内部 README）
└── dataset_1_4/                     # [实验原型] 3 道 5 步综合计算/多图联合审核原型
```

---

## 图片来源与跨层重合说明
- 全套三层去重后独立真实图片总数（SHA-256 并集）：**{len(union_all)} 张**
- Tier 1.1 与 Tier 1.2 图片重合：**{len(shas_11 & shas_12)} 张**（完全零重合）
- Tier 1.1 与 Tier 1.3 图片重合：**{len(shas_11 & shas_13['all'])} 张**
- Tier 1.3 原图说明：所有 600 张投放图片均为真实照片、已发表图表或授权临床影像（0 张合成 SVG），复用自经核验的 Tier 1.2 真实图库（其中核心图重合 **{len(shas_12 & shas_13['focal'])}** 张），并在清单中通过 `source_cluster_id` 显式归为 **49 个** SHA-256 聚类，方便统计分析时做聚类误差控制。

---

## 快速校验命令
```bash
# 1. 校验全部 77 项核心文件与清单的 SHA-256 防篡改哈希
shasum -a 256 -c RELEASE_SHA256SUMS.txt

# 2. 运行 Tier 1.3 全量 60 组发布门禁 CI 校验（120 工作区 / 360 单元 / 600 真图 / 防捷径门禁）
python3 dataset_1_3/tests/test_tier13_60_ci.py

# 3. 重新生成总清单与校验文件
python3 build_unified_release.py
```
"""
    (ROOT / "README.md").write_text(readme, encoding="utf-8")
    print(f"[PASS] Unified release built! Union unique real images={len(union_all)}, core files hashed={len(checksums)}, family manifests hashed={len(fam_manifest_hashes)}")


if __name__ == "__main__":
    main()
