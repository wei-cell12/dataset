---
name: "clinical-screening-approval-gate"
description: "Audit a population disease-screening 2x2 validation table against mandatory sensitivity and specificity thresholds."
---

## Gate Branches
1. `APPROVE_POPULATION_SCREEN`: Applies ONLY when `sensitivity_pct >= 80.0` AND `specificity_pct >= 90.0` (high overall accuracy alone is insufficient under low disease prevalence). Sets `approved_for_screening: true`.
2. `REJECT_LOW_SENSITIVITY`: Applies whenever `sensitivity_pct < 80.0`, regardless of overall accuracy or specificity. Sets `approved_for_screening: false`.
3. `REJECT_LOW_SPECIFICITY`: Applies when `sensitivity_pct >= 80.0` but `specificity_pct < 90.0`.
## Output Format
Return JSON with `sensitivity_pct`, `specificity_pct`, `overall_accuracy_pct`, `gate_branch`, `approved_for_screening`, and `rationale`.
