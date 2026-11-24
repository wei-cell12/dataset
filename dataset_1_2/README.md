# Tier 1.2 — Multimodal Sycophancy & Evidence-Boundary Benchmark (v2.2: 240 Primary Items + 16 Accurate-Draft Companions)

## Core Experimental Principle

**Sole Primary Independent Variable**: **Current-turn user guidance** (neutral no-guidance baseline vs. erroneous/boundary-crossing user guidance vs. evidence-respecting user guidance).

**Three Fixed Operational Context Regimes** (`Skill`, `Memory`, `Pure`): Within every item, the image, background context (skill catalog / preloaded SOP, `retrieved_memory` + `past_dialogue`, or editorial persona + deadline + working draft/note), and neutral de-vaccinated core task/output contract stay **100% byte-identical** across the primary controlled triple.

> **v2.2 Empirical Calibration Upgrade**: Preserves all v2.1 controlled-variable release gates (18/18 programmatic checks) while removing anti-sycophancy audit vaccines from shared base tasks (`Memory` trap-spoiler parentheticals & `Pure` `"Review ... against"` alerts), de-telegraphing 68 1-line `Skill` catalog descriptions for true progressive disclosure (keeping exact preconditions in `SKILL.md` bodies), fixing `T12-M-61` (`adc_map_visible` → `sequence_label_printed`), and upgrading user guidance to natural collaborative workflow directives.

## Exact Primary Distribution Matrix (v2.1 — 240 Primary Items: 720 Primary-Triple + 320 Secondary = 1,040 Prompts)

| Context Regime | Primary Triple (720 prompts) | Secondary Arms (320 prompts) | Chart / Data | Medical | Daily Life | Primary Items | Total Prompts |
|---|---|---|---:|---:|---:|---:|---:|
| **Skill (`skill_80`)** | `N / G- / G+` (240) | `C- / C+` (160) | 27 | 27 | 26 | **80** | 400 |
| **Memory (`memory_80`)** | `M_neutral / M_syco / M_pos` (240) | `M0` (`include_memory: false`, 80) | 27 | 26 | 27 | **80** | 320 |
| **Pure (`pure_80`)** | `P0 / P_auth / P_pos` (240) | `P_soft` (80) + 16 companions (48) | 26 | 27 | 27 | **80** | 320 (+48 companion) |
| **Total** | **720 primary-triple** | **320 secondary (+48 companion)** | **80** | **80** | **80** | **240** | **1,040 (+48)** |

## Key v2.1 Methodological Guarantees

1. **Memory (`memory_80`, 80 items)**:
   - `M0` and `M_neutral` share the **exact byte-identical `core_task`** across 80/80 items (zero prompt-length or policy-removal confound).
   - `retrieved_memory` and `past_dialogue` (160/160 turns carry non-empty `session` metadata) are scoped to past personal/private notes without answer-rehearsing caveats or current-image payloads, and stay 100% identical across `M_neutral`, `M_syco`, `M_pos`.
   - `M_syco` appends one **preference-based guidance sentence** (leaving the factual decision open), while `M_pos` appends one **non-leaky evidence-respecting guidance sentence** (zero item answers revealed).
2. **Skill (`skill_80`, 80 items, 320 reusable `SKILL.md` SOPs)**:
   - Uniform **5-skill pools** across all 60 catalog items (`mode1`, `mode2`, `mode4`) with **shuffled, quota-balanced gold-slot placement (`0..4`)** frozen identically across `N / C- / G- / C+ / G+`.
   - **Uniform Mode 2 selection phrasing** across all 20 items (`10 ABSTAIN_NONE / 10 VALID_APPLICABLE`, eliminating text-only prompt shortcuts), plus **exact 50/50 decision polarity** in Mode 3 (`10 FAVORABLE_APPROVE / 10 UNFAVORABLE_REJECT_HOLD`) and Mode 4 (`10 HOLD_PREREQUISITE / 10 PROCEED_DIRECT`).
   - **Reusable domain SOPs** across all 320 `SKILL.md` files (item-specific dates/observations removed; SOP output schemas aligned with `gold_expected`), and **exact one-identifier substitution** between `G-` and `G+` across 80/80 items.
3. **Pure (`pure_80`, 80 primary items + 16 accurate-draft companions)**:
   - Unified Option X design: persona, deadline, output contract, and exact draft/proposed summary are **100% byte-identical** across `P0`, `P_auth`, `P_pos`, with zero item answers supplied in `P_pos`.
   - Companion rewritten-draft preservation control ([accurate_draft_companion_16.json](pure_80/accurate_draft_companion_16.json), 4 per Pure mode, preserving exact paired pre-draft output contracts) kept strictly outside the 80-item primary erroneous-guidance denominator.
4. **Data Integrity**:
   - **240 unique SHA-256 real public images**, **0 overlap** with Tier 1.1 (`229` unique images; `469` unique images combined).
   - Full cohort × domain × source provenance recorded transparently in `tier_1_2_manifest_240.json`.

## Key Files

- `benchmark_1_2_240.json` — Unified v2.1 240-item primary benchmark + 320-skill catalog
- `tier_1_2_manifest_240.json` — Programmatic release-gate audit manifest & cohort × domain × dataset breakdown
- `tier_1_2_240_overview.csv` — Flat 240-row item table
- `skill_80/benchmark_1_2_skill_80.json` — Standalone 80-item Skill module (+ `images/`, `skills/`)
- `memory_80/benchmark_1_2_memory_80.json` — Standalone 80-item Memory module (+ `images/`)
- `pure_80/benchmark_1_2_pure_80.json` & `pure_80/accurate_draft_companion_16.json` — Standalone 80-item Pure module + 16 accurate-draft companions (+ `images/`)
- `scale_240/eval_tier12_240.py` — Unified resumable v2.1 evaluator (true two-stage Skill execution, frozen `catalog_order`, strict Mode-3 JSON branch parsing, `--ablate-image` support, stratified `smoke24` + full 240/256/1,088 suites)
- `scale_240/score_tier12_240.py` — Portable, zero-hardcode, condition-blinded automated scorer & statistical reporter (95% Wilson CIs, paired transitions, exact two-sided McNemar p-values, Stage 1 vs Stage 2, 12-mode / 3-domain / 50-50 polarity / cohort / format breakdowns)

## Evaluation & Scoring Quickstart

```bash
# 1. Stratified 28-item smoke pilot (24 primary + 4 companion = 84 primary-triple runs)
python3 scale_240/eval_tier12_240.py --model gemini-3.8-flash-low --suite smoke24 --workers 8

# 2. Full 240 primary items + 16 accurate-draft companions (768 primary-triple runs)
python3 scale_240/eval_tier12_240.py --model gemini-3.8-flash-low --suite primary_plus_companion --workers 8

# 3. Text-only visual-grounding ablation baseline
python3 scale_240/eval_tier12_240.py --model gemini-3.8-flash-low --suite primary --ablate-image --workers 8

# 4. Condition-blinded automated scoring & Markdown/CSV/JSON report generation
python3 scale_240/score_tier12_240.py eval_results_240/eval_gemini-3.8-flash-low_smoke24.json --judge-model gemini-3.8-flash-low --workers 8
```
