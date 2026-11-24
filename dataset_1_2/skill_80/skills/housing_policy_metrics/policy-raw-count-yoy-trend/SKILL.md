---
name: "policy-raw-count-yoy-trend"
description: "Compute multi-year absolute and percentage changes from annual public-sector headcount charts."
---

## When This Skill Applies
Use when a public-sector chart plots raw annual counts over multiple years and the task requests raw headcount growth trends.
## Procedure
1. Read approximate raw counts for each plotted year (noting visual tolerance where exact bar labels are absent).
2. Compute start-to-end absolute and percentage growth plus directional year-by-year shifts.
3. Emit JSON with `METRIC_BASIS: RAW_ANNUAL_COUNTS`, `start_year`, `end_year`, `approx_growth_pct`, and `notes`.
