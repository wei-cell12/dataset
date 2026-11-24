---
name: "commodity-multiyear-cagr"
description: "Calculate compound annual growth rates (CAGR) from multi-year commodity price time-series line charts."
---

## When This Skill Applies
Use for multi-year line charts displaying start-year and end-year price curves over time.

## Procedure
1. Extract start value, end value, and elapsed years `n`.
2. Compute `CAGR = (end / start)^(1/n) - 1` and report annualized growth rates.
