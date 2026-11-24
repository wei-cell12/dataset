# Multimodal Sycophancy & Evidence-Boundary Benchmark Suite (`v1.0-frozen`)

A three-tier, 100% real-image multimodal benchmark measuring how vision-language models and tool-using agents handle user sycophancy pressure and evidence boundaries — progressing from direct single-image contradiction (**Tier 1.1**), to single-turn evidence-boundary / skill / memory conflicts (**Tier 1.2**), to long-context 3-hop multi-file multi-image agent workspaces (**Tier 1.3**).

## Suite Overview

| Tier | Version | Scale | Domains | Images | Independent Audit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tier 1.1** (`dataset_1_1/`) | `tier1.1-125-v1.1` | **125 items** (3 original arms + 5 unified aligned conditions) | `daily_life` (50), `medical` (50), `chart_data` (25) | **125** unique real images (`0` overlap w/ 1.2) | 125/125 SHA-256 verified |
| **Tier 1.2** (`dataset_1_2/`) | `tier1.2-240-v2.2` | **240 primary + 16 accurate-draft companions = 256 items** (1,088 prompts across Pure / Skill / Memory) | `daily_life` (80), `medical` (80), `chart_data` (80) | **240** unique primary real images | **GPT 6.2 Astra: 8.5/10** (dataset+harness) |
| **Tier 1.3** (`dataset_1_3/`) | `tier1.3-60-v2.8` | **60 families = 120 twin workspaces (`U/V`) = 360 primary episodes/model (`N/A/Q × U/V`)** + 12 balanced Short-Evidence Controls (`6U/6V`) | `daily_life` (20), `medical` (20), `chart_data` (20) × 4 archetypes | **600** real image placements (181 unique SHA-256, 49 source clusters, **0 SVGs**) | **GPT 6.2 Astra: 9/10 Pass** (zero-shortcut verified) |

## Key Release Files
- **Master Manifest**: `UNIFIED_BENCHMARK_MANIFEST.json`
- **Tamper-Evident Checksums**: `RELEASE_SHA256SUMS.txt` (verify with `shasum -a 256 -c RELEASE_SHA256SUMS.txt`)
- **Tier 1.1**: `dataset_1_1/benchmark_1_1_aligned.json` (plus original `dataset_1_1/benchmark_1_1.json`) & `dataset_1_1/tier_1_1_manifest.json`
- **Tier 1.2**: `dataset_1_2/benchmark_1_2_240.json` & `dataset_1_2/tier_1_2_manifest_240.json`
- **Tier 1.3**: `dataset_1_3/families_60/` & `dataset_1_3/tier_1_3_manifest_60.json`

## Image Provenance & Cross-Tier Overlap Disclosure
- Total unique real images across the suite (SHA-256 union): **423**
- Tier 1.1 ↔ Tier 1.2 image overlap: **0**
- Tier 1.1 ↔ Tier 1.3 image overlap: **0**
- Tier 1.2 ↔ Tier 1.3 focal image reuse: **104** (all Tier 1.3 images are genuine photographs, published charts, or licensed clinical scans drawn from the verified Tier 1.2 real-image pool; shared-source families are grouped via `source_cluster_id` into **49** SHA-256 clusters for clustered statistical analysis).

## Verification Commands
```bash
# 1. Verify all release SHA-256 checksums
shasum -a 256 -c RELEASE_SHA256SUMS.txt

# 2. Run full Tier 1.3 60-family release-gate CI (120 workspaces, 360 cells, 600 images, anti-shortcut & parser gates)
python3 dataset_1_3/tests/test_tier13_60_ci.py

# 3. Rebuild unified release manifest & checksums
python3 build_unified_release.py
```
