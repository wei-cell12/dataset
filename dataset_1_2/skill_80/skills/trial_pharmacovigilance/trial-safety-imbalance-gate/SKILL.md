---
name: "trial-safety-imbalance-gate"
description: "Audit vaccine-versus-placebo adverse-event incidence rates from a randomized clinical trial safety table to emit a safety-gate JSON."
---

## When This Skill Applies
Use to evaluate whether a trial safety summary table exhibits an excess adverse-event rate in the Vaccination arm compared to the Placebo arm.

## Extracted Evidence
Read arm denominators (`n_vaccine`, `n_placebo`) and compute percentage incidence (`count / arm_n * 100`) for every printed adverse-event row:
- `serious_ae_28d_pct`: `{"vaccine": ..., "placebo": ...}`
- `serious_ae_14m_pct`: `{"vaccine": ..., "placebo": ...}`
- `any_ae_7d_pct`: `{"vaccine": ..., "placebo": ...}`
- `tertiary_ae_pct`: `{"vaccine": ..., "placebo": ...}`
- `excess_risk_rows`: count of rows where Vaccine incidence % strictly exceeds Placebo incidence %

## Safety Gate Branches
Assign `release_branch` strictly from normalized arm incidence percentages (NEVER from raw unnormalized event counts alone):
1. `SAFETY_PARITY_PASS`:
   - Applies when Vaccine percentage incidence is `<=` Placebo percentage incidence in ALL four printed adverse-event rows (`excess_risk_rows == 0`).
   - Sets `hold_recommended: false`.
2. `SAFETY_SIGNAL_HOLD`:
   - Applies ONLY when Vaccine percentage incidence exceeds Placebo percentage incidence by `>= 2.0` percentage points in any row, OR exceeds Placebo by `>= 0.5` percentage points in either Serious Adverse Event row.
   - Sets `hold_recommended: true`.
3. `MINOR_EXCESS_MONITOR`:
   - Applies when `excess_risk_rows >= 1` but excess stays below the `SAFETY_SIGNAL_HOLD` thresholds.
   - Sets `hold_recommended: false`.

## Output Format
Return a single JSON object with keys `n_vaccine`, `n_placebo`, `serious_ae_28d_pct`, `serious_ae_14m_pct`, `any_ae_7d_pct`, `tertiary_ae_pct`, `excess_risk_rows`, `release_branch`, `hold_recommended`, and `rationale`.
