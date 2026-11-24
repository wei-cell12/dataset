---
name: "project-risk-efficiency-gate"
description: "Audit a candidate mutually exclusive capital project for mean-variance dominance and Coefficient of Variation (CV = SD / Expected Return)."
---

## Gate Branches
1. `APPROVE_PROJECT`: Applies ONLY when Expected Return >= 12.0% AND no competing project achieves strictly higher return with strictly lower SD (and lower CV). Sets `approved: true`.
2. `REJECT_HIGHER_CV_DOMINATED`: Applies whenever another competing project achieves strictly higher return at strictly lower SD (and lower CV). Sets `approved: false` and `dominating_project: <name>`.
## Output Format
Return JSON with `candidate_project`, `candidate_cv`, `dominating_project`, `dominating_cv`, `gate_branch`, `approved`, and `rationale`.
