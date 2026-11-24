# Tier 1.3 Multimodal Multi-File Workspace Benchmark (`tier1.3-60-v2.8`)

## Overview
- **Confirmatory Set (`families_60/`)**: **60 scenario families** = **120 workspaces (`U/V` twins)** = **360 primary episodes per model (`N / A / Q × U / V`)**, plus **12 preselected balanced Short-Evidence Control families** (72 additional episodes/model).
- **Balanced 3 × 4 Matrix**: `3 domains` (`daily_life`, `chart_data`, `medical`) × `4 archetypes` (`visual_record_reconciliation`, `effective_state`, `procedure_applicability`, `entity_scope_linkage`) × `5 families per cell = 60`.
- **100% Real Images & Provenance Disclosure**:
  - All **600 images** (`60 × 2 branches × 5 unique images`) are real photographs, real published charts/tables (Pew / OWID / OECD / Finance), or real licensed clinical scans — **0 synthetic SVGs**, 100% PNG/JPEG magic-byte verified.
  - Focal and distractor images are drawn from the verified Tier 1.2 real-image pool (`dataset_1_2/`). Families sharing any focal image filename or SHA-256 hash are grouped into connected **`source_cluster_id`** clusters (recorded in `tier_1_3_manifest_60.json` and every `manifest.json`) so downstream statistical analyses can cluster standard errors / treat shared-source families as related.
- **Anti-Shortcut 3-Hop Cross-Modal Chain**:
  1. **Independent Random Opaque IDs**: `ticket_id` sampled without replacement from `TK-3100..TK-8899` (zero relation to family index, target, or filename).
  2. **Hop 1 (`records/intake_queue.csv`, 145 rows, randomized decisive line ≥ 125)**: maps `ticket_id -> (track_code, asset_file)`.
  3. **Hop 2 (`operations/track_charter.csv`, 140 rows, randomized decisive line ≥ 122)**: **6 competing rows sharing identical decision labels**, with the real row placed at a balanced random slot (`0..5`, 10 each) AND its `track_code` sampled from the same unified numerical pool (`100..889`) with balanced numerical rank (`0..5`, 10 each) so neither row position nor min/max code heuristics can bypass Hop 1; paired with `procedures/review_protocol.md`.
  4. **Hop 3 (5 unique real images, 3 same-date `20261118` candidates)**: assigned image placed at a balanced random slot (`a`/`b`/`c`, 20 each); reconcile pixels of `asset_file` against `required_target`.
- **Counterbalanced Memory Prior**: Exactly **30 U-prior / 30 V-prior** (`10 U / 10 V` in every domain).

## Quick Commands
```bash
# Rebuild all 60 families + top-level manifest
python3 builders/build_tier13_60.py

# Run full 60-family release-gate CI verification
python3 tests/test_tier13_60_ci.py

# Evaluate a model on all 60 families (360 episodes)
python3 eval/eval_tier13.py --model gpt-5.6-luna --runner codex --families-dir families_60 --tag conf60_v22 --workers 5
```
