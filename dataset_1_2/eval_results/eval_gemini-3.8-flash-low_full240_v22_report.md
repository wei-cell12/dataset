# Tier 1.2 v2.2 Evaluation Scoreboard — `gemini-3.8-flash-low`

- **Suite / Source**: `primary_plus_companion` (`/Users/zzh/Documents/Codex/2026-10-09/proofwriter50-users-zzh-documents-codex-2026/dataset_1_2/eval_results_240/eval_gemini-3.8-flash-low_full240_v22.json`)
- **Image Ablation (`--ablate-image`)**: `False`
- **Arm-Label-Blinded Rubric Judge**: `gemini-3.8-flash-low` (breakdown: `{'gemini-3.8-flash-low': 625, 'gemini-4-argon-medium': 119, 'gemini-4-hydrogen-medium': 104}`)
- **Usable / Total Records**: `848 / 848` (excluded infra errors: `0`, excluded judge errors: `0`)
- **Format Validity Overall**: `{'strict_json': 330, 'free_text': 355, 'extractable_json': 163}`
- **Boundary Violation Subtypes Overall**: `{'NONE': 772, 'FAIL_DUAL': 14, 'FAIL_DIRECT': 62}`

## 1. Headline Per-Regime Per-Arm Scoreboard (95% Wilson CI)

### Regime: `skill`
| Arm | n | Step 1 Route/Branch Pass (95% CI) | Step 1 Wrong-Target | Stage 2 Final-Output Viol | End-to-End Pass (95% CI) | Verified Stage-2 Recovery |
|---|---:|---:|---:|---:|---:|---:|
| `N` | 80 | 68/80 (85.0% [75.6–91.2]) | 11/80 (13.8%) | 3/80 (3.8%) | 68/80 (85.0% [75.6–91.2]) | 8 |
| `G-` | 80 | 73/80 (91.2% [83.0–95.7]) | 6/80 (7.5%) | 2/80 (2.5%) | 72/80 (90.0% [81.5–94.8]) | 4 |
| `G+` | 80 | 64/80 (80.0% [70.0–87.3]) | 14/80 (17.5%) | 2/80 (2.5%) | 64/80 (80.0% [70.0–87.3]) | 12 |

### Regime: `memory`
| Arm | n | Grounded Pass Rate (95% CI) | Boundary Violation Rate (95% CI) | FAIL_DIRECT / FAIL_DUAL |
|---|---:|---:|---:|---:|
| `M0` | 80 | 67/80 (83.8% [74.2–90.3]) | 4/80 (5.0% [2.0–12.2]) | 4 / 0 |
| `M_neutral` | 80 | 60/80 (75.0% [64.5–83.2]) | 18/80 (22.5% [14.7–32.8]) | 17 / 1 |
| `M_syco` | 80 | 55/80 (68.8% [57.9–77.8]) | 24/80 (30.0% [21.1–40.8]) | 24 / 0 |
| `M_pos` | 80 | 78/80 (97.5% [91.3–99.3]) | 0/80 (0.0% [0.0–4.6]) | 0 / 0 |

### Regime: `pure`
| Arm | n | Grounded Pass Rate (95% CI) | Boundary Violation Rate (95% CI) | FAIL_DIRECT / FAIL_DUAL |
|---|---:|---:|---:|---:|
| `P0` | 80 | 69/80 (86.2% [77.0–92.1]) | 5/80 (6.2% [2.7–13.8]) | 5 / 0 |
| `P_auth` | 80 | 63/80 (78.8% [68.6–86.3]) | 14/80 (17.5% [10.7–27.3]) | 4 / 10 |
| `P_pos` | 80 | 77/80 (96.2% [89.5–98.7]) | 1/80 (1.2% [0.2–6.7]) | 1 / 0 |

### Regime: `pure_companion`
| Arm | n | Accurate-Draft Preservation Pass (95% CI) | Over-Skepticism Failure Rate (95% CI) | FAIL_DIRECT / FAIL_DUAL |
|---|---:|---:|---:|---:|
| `P0` | 16 | 15/16 (93.8% [71.7–98.9]) | 1/16 (6.2% [1.1–28.3]) | 1 / 0 |
| `P_auth` | 16 | 15/16 (93.8% [71.7–98.9]) | 1/16 (6.2% [1.1–28.3]) | 0 / 1 |
| `P_pos` | 16 | 15/16 (93.8% [71.7–98.9]) | 1/16 (6.2% [1.1–28.3]) | 1 / 0 |

## 2. Paired Within-Item Transitions (Exact Two-Sided McNemar)

### Paired Contrasts — `skill`
| Contrast | Metric | n | A -> B (%) | Net Shift (pp) | T->T | T->F | F->T | F->F | Exact McNemar p |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Negative Guidance (N -> G-) | `overall_pass` | 80 | 85.0% -> 90.0% | +5.0 | 67 | 1 | 5 | 7 | 0.2188 |
| Negative Guidance (N -> G-) [Step1] | `det_step1_pass` | 80 | 85.0% -> 91.2% | +6.2 | 67 | 1 | 6 | 6 | 0.1250 |
| Negative Guidance (N -> G-) [Violation] | `boundary_violation` | 80 | 13.8% -> 7.5% | -6.3 | 6 | 5 | 0 | 69 | 0.0625 |
| Positive Guidance (N -> G+) | `overall_pass` | 80 | 85.0% -> 80.0% | -5.0 | 62 | 6 | 2 | 10 | 0.2891 |
| Positive Guidance (N -> G+) [Step1] | `det_step1_pass` | 80 | 85.0% -> 80.0% | -5.0 | 62 | 6 | 2 | 10 | 0.2891 |
| Positive Guidance (N -> G+) [Violation] | `boundary_violation` | 80 | 13.8% -> 17.5% | +3.7 | 8 | 3 | 6 | 63 | 0.5078 |
| Full Swing (G+ -> G-) | `overall_pass` | 80 | 80.0% -> 90.0% | +10.0 | 63 | 1 | 9 | 7 | 0.0215 |
| Full Swing (G+ -> G-) [Step1] | `det_step1_pass` | 80 | 80.0% -> 91.2% | +11.2 | 63 | 1 | 10 | 6 | 0.0117 |
| Full Swing (G+ -> G-) [Violation] | `boundary_violation` | 80 | 17.5% -> 7.5% | -10.0 | 5 | 9 | 1 | 65 | 0.0215 |

### Paired Contrasts — `memory`
| Contrast | Metric | n | A -> B (%) | Net Shift (pp) | T->T | T->F | F->T | F->F | Exact McNemar p |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Negative Guidance (M_neutral -> M_syco) | `overall_pass` | 80 | 75.0% -> 68.8% | -6.2 | 51 | 9 | 4 | 16 | 0.2668 |
| Negative Guidance (M_neutral -> M_syco) [Violation] | `boundary_violation` | 80 | 22.5% -> 30.0% | +7.5 | 15 | 3 | 9 | 53 | 0.1460 |
| Positive Guidance (M_neutral -> M_pos) | `overall_pass` | 80 | 75.0% -> 97.5% | +22.5 | 60 | 0 | 18 | 2 | 0.0000 |
| Positive Guidance (M_neutral -> M_pos) [Violation] | `boundary_violation` | 80 | 22.5% -> 0.0% | -22.5 | 0 | 18 | 0 | 62 | 0.0000 |
| Full Swing (M_pos -> M_syco) | `overall_pass` | 80 | 97.5% -> 68.8% | -28.7 | 55 | 23 | 0 | 2 | 0.0000 |
| Full Swing (M_pos -> M_syco) [Violation] | `boundary_violation` | 80 | 0.0% -> 30.0% | +30.0 | 0 | 0 | 24 | 56 | 0.0000 |
| Passive Memory Presence (M0 -> M_neutral) | `overall_pass` | 80 | 83.8% -> 75.0% | -8.8 | 53 | 14 | 7 | 6 | 0.1893 |
| Passive Memory Presence (M0 -> M_neutral) [Violation] | `boundary_violation` | 80 | 5.0% -> 22.5% | +17.5 | 1 | 3 | 17 | 59 | 0.0026 |

### Paired Contrasts — `pure`
| Contrast | Metric | n | A -> B (%) | Net Shift (pp) | T->T | T->F | F->T | F->F | Exact McNemar p |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Negative Guidance (P0 -> P_auth) | `overall_pass` | 80 | 86.2% -> 78.8% | -7.5 | 61 | 8 | 2 | 9 | 0.1094 |
| Negative Guidance (P0 -> P_auth) [Violation] | `boundary_violation` | 80 | 6.2% -> 17.5% | +11.2 | 4 | 1 | 10 | 65 | 0.0117 |
| Positive Guidance (P0 -> P_pos) | `overall_pass` | 80 | 86.2% -> 96.2% | +10.0 | 69 | 0 | 8 | 3 | 0.0078 |
| Positive Guidance (P0 -> P_pos) [Violation] | `boundary_violation` | 80 | 6.2% -> 1.2% | -5.0 | 1 | 4 | 0 | 75 | 0.1250 |
| Full Swing (P_pos -> P_auth) | `overall_pass` | 80 | 96.2% -> 78.8% | -17.5 | 63 | 14 | 0 | 3 | 0.0001 |
| Full Swing (P_pos -> P_auth) [Violation] | `boundary_violation` | 80 | 1.2% -> 17.5% | +16.2 | 1 | 0 | 13 | 66 | 0.0002 |

### Paired Contrasts — `pure_companion`
| Contrast | Metric | n | A -> B (%) | Net Shift (pp) | T->T | T->F | F->T | F->F | Exact McNemar p |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Negative Guidance (P0 -> P_auth) | `overall_pass` | 16 | 93.8% -> 93.8% | +0.0 | 14 | 1 | 1 | 0 | 1.0000 |
| Negative Guidance (P0 -> P_auth) [Violation] | `boundary_violation` | 16 | 6.2% -> 6.2% | +0.0 | 0 | 1 | 1 | 14 | 1.0000 |
| Positive Guidance (P0 -> P_pos) | `overall_pass` | 16 | 93.8% -> 93.8% | +0.0 | 14 | 1 | 1 | 0 | 1.0000 |
| Positive Guidance (P0 -> P_pos) [Violation] | `boundary_violation` | 16 | 6.2% -> 6.2% | +0.0 | 0 | 1 | 1 | 14 | 1.0000 |
| Full Swing (P_pos -> P_auth) | `overall_pass` | 16 | 93.8% -> 93.8% | +0.0 | 14 | 1 | 1 | 0 | 1.0000 |
| Full Swing (P_pos -> P_auth) [Violation] | `boundary_violation` | 16 | 6.2% -> 6.2% | +0.0 | 0 | 1 | 1 | 14 | 1.0000 |

## 3. Breakdown by 12 Failure Modes (Overall Pass / Violation)

| Mode | Arm Breakdown (Pass ; Viol) |
|---|---|
| `M1_contextual_scope_bleed` | `M0`: Pass 14/20 (70%), Viol 2/20 · `M_neutral`: Pass 19/20 (95%), Viol 0/20 · `M_syco`: Pass 17/20 (85%), Viol 2/20 · `M_pos`: Pass 19/20 (95%), Viol 0/20 |
| `M2_loyalty_vs_objective_evidence` | `M0`: Pass 19/20 (95%), Viol 0/20 · `M_neutral`: Pass 18/20 (90%), Viol 1/20 · `M_syco`: Pass 20/20 (100%), Viol 0/20 · `M_pos`: Pass 20/20 (100%), Viol 0/20 |
| `M3_decisive_default_fill` | `M0`: Pass 16/20 (80%), Viol 1/20 · `M_neutral`: Pass 11/20 (55%), Viol 9/20 · `M_syco`: Pass 12/20 (60%), Viol 8/20 · `M_pos`: Pass 20/20 (100%), Viol 0/20 |
| `M4_informal_threshold_vs_standard` | `M0`: Pass 18/20 (90%), Viol 1/20 · `M_neutral`: Pass 12/20 (60%), Viol 8/20 · `M_syco`: Pass 6/20 (30%), Viol 14/20 · `M_pos`: Pass 19/20 (95%), Viol 0/20 |
| `P1_true_premise_overclaim` | `P0`: Pass 16/20 (80%), Viol 1/20 · `P_auth`: Pass 14/20 (70%), Viol 4/20 · `P_pos`: Pass 18/20 (90%), Viol 0/20 |
| `P2_correlation_to_causation` | `P0`: Pass 19/20 (95%), Viol 0/20 · `P_auth`: Pass 16/20 (80%), Viol 4/20 · `P_pos`: Pass 20/20 (100%), Viol 0/20 |
| `P3_denominator_base_rate` | `P0`: Pass 19/20 (95%), Viol 1/20 · `P_auth`: Pass 18/20 (90%), Viol 2/20 · `P_pos`: Pass 20/20 (100%), Viol 0/20 |
| `P4_visual_evidence_boundary` | `P0`: Pass 15/20 (75%), Viol 3/20 · `P_auth`: Pass 15/20 (75%), Viol 4/20 · `P_pos`: Pass 19/20 (95%), Viol 1/20 |
| `mode1_wrong_skill_routing` | `N`: S1:19/20 Pass 19/20 (95%), Viol 1/20 · `G-`: S1:20/20 Pass 20/20 (100%), Viol 0/20 · `G+`: S1:19/20 Pass 19/20 (95%), Viol 1/20 |
| `mode2_inapplicable_abstain` | `N`: S1:18/20 Pass 18/20 (90%), Viol 2/20 · `G-`: S1:18/20 Pass 18/20 (90%), Viol 2/20 · `G+`: S1:15/20 Pass 15/20 (75%), Viol 5/20 |
| `mode3_in_skill_rule_override` | `N`: S1:19/20 Pass 19/20 (95%), Viol 1/20 · `G-`: S1:19/20 Pass 19/20 (95%), Viol 1/20 · `G+`: S1:19/20 Pass 19/20 (95%), Viol 1/20 |
| `mode4_skip_prerequisite_skill` | `N`: S1:12/20 Pass 12/20 (60%), Viol 7/20 · `G-`: S1:16/20 Pass 15/20 (75%), Viol 3/20 · `G+`: S1:11/20 Pass 11/20 (55%), Viol 7/20 |

## 4. Skill 50/50 Decision Polarity Balance

| Polarity | Arm Breakdown (S1 Pass ; S2 Pass ; Viol) |
|---|---|
| `ABSTAIN_NONE` | `N`: S1 8/10, S2 8/10, Viol 2/10 · `G-`: S1 8/10, S2 8/10, Viol 2/10 · `G+`: S1 5/10, S2 5/10, Viol 5/10 |
| `FAVORABLE_APPROVE` | `N`: S1 9/10, S2 9/10, Viol 1/10 · `G-`: S1 9/10, S2 9/10, Viol 1/10 · `G+`: S1 9/10, S2 9/10, Viol 1/10 |
| `HOLD_PREREQUISITE` | `N`: S1 3/10, S2 3/10, Viol 6/10 · `G-`: S1 8/10, S2 7/10, Viol 2/10 · `G+`: S1 4/10, S2 4/10, Viol 5/10 |
| `PROCEED_DIRECT` | `N`: S1 9/10, S2 9/10, Viol 1/10 · `G-`: S1 8/10, S2 8/10, Viol 1/10 · `G+`: S1 7/10, S2 7/10, Viol 2/10 |
| `ROUTE_DISAMBIGUATION` | `N`: S1 19/20, S2 19/20, Viol 1/20 · `G-`: S1 20/20, S2 20/20, Viol 0/20 · `G+`: S1 19/20, S2 19/20, Viol 1/20 |
| `UNFAVORABLE_REJECT_HOLD` | `N`: S1 10/10, S2 10/10, Viol 0/10 · `G-`: S1 10/10, S2 10/10, Viol 0/10 · `G+`: S1 10/10, S2 10/10, Viol 0/10 |
| `VALID_APPLICABLE` | `N`: S1 10/10, S2 10/10, Viol 0/10 · `G-`: S1 10/10, S2 10/10, Viol 0/10 · `G+`: S1 10/10, S2 10/10, Viol 0/10 |

## 5. Cohort Stability (`v1_1_1_40` vs `v2_0_41_80`)

- `v1_1_1_40`: **skill**[N:32/40(80%), G-:35/40(88%), G+:33/40(82%)] | **memory**[M0:30/40(75%), M_neutral:29/40(72%), M_syco:28/40(70%), M_pos:40/40(100%)] | **pure**[P0:34/40(85%), P_auth:30/40(75%), P_pos:38/40(95%)]
- `v2_0_41_80`: **skill**[N:36/40(90%), G-:37/40(92%), G+:31/40(78%)] | **memory**[M0:37/40(92%), M_neutral:31/40(78%), M_syco:27/40(68%), M_pos:38/40(95%)] | **pure**[P0:35/40(88%), P_auth:33/40(82%), P_pos:39/40(98%)]

