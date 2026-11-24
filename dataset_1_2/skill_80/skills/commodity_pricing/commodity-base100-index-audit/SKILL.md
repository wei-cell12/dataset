---
name: "commodity-base100-index-audit"
description: "Audit historical food-commodity index charts and compute baseline-relative real index changes."
---

## When This Skill Applies
Use for commodity bar charts reporting historical price indices normalized to a base year (`base = 100`) for a single snapshot year.
## Preconditions
- Bar values are dimensionless base-100 index points rather than currency prices per unit.
## Procedure
1. Record the snapshot year and base-year definition printed on the chart.
2. For each requested commodity, extract its index `I` and compute real percent change from base: `pct_vs_base = round(I - 100, 2)`.
3. Compute `top_to_bottom_ratio = round(I_max / I_min, 2)`.
4. Set `UNIT_BASIS: REAL_INDEX_BASE_100` and state that values represent index levels rather than nominal USD prices.
5. Output a concise pricing brief listing each item's index, `pct_vs_base`, `top_to_bottom_ratio`, snapshot year, and `UNIT_BASIS`.
