---
name: "timeseries-annual-yoy-continuous"
description: "Compute consecutive year-over-year annual deltas across every calendar year in a continuous time series and verify exhaustive 100% annual totals."
---

## When This Skill Applies
Use when a polling time-series chart reports every consecutive calendar year without gaps and displays all exhaustive response categories summing to 100%.

## Output Format
Return a JSON object with consecutive `yoy_deltas` for every year pair and `exhaustive_sum_check`.
