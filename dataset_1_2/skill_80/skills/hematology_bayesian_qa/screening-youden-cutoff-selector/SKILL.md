---
name: "screening-youden-cutoff-selector"
description: "Select the optimal diagnostic cutoff maximizing Youden's Index (`Sensitivity + Specificity - 100%`) from a sensitivity/specificity threshold table."
---

## When This Skill Applies
Use when a table lists diagnostic thresholds alongside printed Sensitivity (%) and Specificity (%) and the task requests selecting the optimal cutoff by Youden's Index (which does not require prevalence).
## Procedure
1. Compute `J = Sensitivity + Specificity - 100` for each printed cutoff.
2. Identify the cutoff maximizing `J`.
3. Emit JSON with `CUTOFF_BASIS: YOUDEN_J_MAX`.
