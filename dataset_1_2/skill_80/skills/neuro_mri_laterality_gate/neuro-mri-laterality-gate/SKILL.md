---
name: "neuro-mri-laterality-gate"
description: "Audit a proposed unilateral hemisphere MRI draft report against image laterality markers and bilateral finding distribution."
---

## Gate Branches
1. `APPROVE_UNILATERAL_LEFT_REPORT`: Applies ONLY when an explicit `R`/`L` laterality marker is stamped on the image AND hyperintensity is strictly confined to the verified left hemisphere. Sets `report_approved: true`.
2. `HOLD_MISSING_LATERALITY_QA`: Applies whenever NO `R`/`L` laterality marker is printed on the slice OR bright signal changes appear bilaterally in both hemispheres. Sets `report_approved: false`.
## Output Format
Return JSON with `rl_marker_printed`, `bilateral_signal_visible`, `gate_branch`, `report_approved`, and `rationale`.
