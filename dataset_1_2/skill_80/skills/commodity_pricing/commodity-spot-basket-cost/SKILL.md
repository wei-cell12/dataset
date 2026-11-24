---
name: "commodity-spot-basket-cost"
description: "Summarize food-commodity pricing comparisons and basket averages from commodity bar charts."
---

## When This Skill Applies
Use for wholesale commodity bar charts displaying nominal USD spot prices per standard unit.

## Preconditions
- Bar values represent nominal USD prices per unit.

## Procedure
1. Extract the nominal USD spot price for each requested commodity.
2. Compute `basket_total_usd` (sum) and `mean_unit_price_usd` (average), rounded to 2 decimals.
3. Set `UNIT_BASIS: NOMINAL_USD_SPOT` and output a concise procurement cost brief.
