---
name: "biostat-predictor-inclusion-gate"
description: "Evaluate a regression predictor's coefficient and standard error to decide statistical retention."
---

## Gate Branches
1. `RETAIN_SIGNIFICANT_PREDICTOR`: Applies ONLY when `|b / SE| >= 1.96`. Sets `retain_predictor: true`.
2. `DROP_NONSIGNIFICANT`: Applies whenever `|b / SE| < 1.96`, even if the point estimate has the expected clinical sign. Sets `retain_predictor: false`.
## Output Format
Return JSON with `predictor`, `b_hat`, `se`, `t_stat`, `gate_branch`, `retain_predictor`, and `rationale`.
