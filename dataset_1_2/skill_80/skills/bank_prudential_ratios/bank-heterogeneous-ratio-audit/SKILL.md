---
name: "bank-heterogeneous-ratio-audit"
description: "Audit multi-indicator banking regulation bar charts whose percentages use heterogeneous denominators (capital, loans, liabilities, assets)."
---

## When This Skill Applies
Use when percentage bars measure distinct financial ratios with different denominators (often exceeding 100%).
## Procedure
1. Record each indicator, its printed percentage, and its distinct denominator.
2. Set `BASIS_TAG: MIXED_DENOMINATOR_RATIOS` and prohibit summing ratios across bars.
3. Return compact JSON with `country`, `year`, `ratios`, and `BASIS_TAG`.
