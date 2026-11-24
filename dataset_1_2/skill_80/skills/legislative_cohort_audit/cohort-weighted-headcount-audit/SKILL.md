---
name: "cohort-weighted-headcount-audit"
description: "Compute headcount-weighted demographic cohort averages from subgroup charts and tables."
---

## When This Skill Applies
Use when both per-group shares and subgroup headcount denominators are printed on the figure.
## Procedure
1. Multiply each subgroup share by its printed headcount.
2. Divide total weighted numerator by total headcount.
3. Emit structured weighted-average JSON.
