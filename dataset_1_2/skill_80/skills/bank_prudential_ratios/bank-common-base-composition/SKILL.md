---
name: "bank-common-base-composition"
description: "Aggregate percentage-composition bar charts whose segments partition a single 100% balance-sheet base."
---

## When This Skill Applies
Use ONLY when all bars share a single denominator and sum to a common 100% total.
## Procedure
1. Sum all bar percentages and compute each share of the total.
2. Set `BASIS_TAG: COMMON_BASE_SUM` and return JSON.
