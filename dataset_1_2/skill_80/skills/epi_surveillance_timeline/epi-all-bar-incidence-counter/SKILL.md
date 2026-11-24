---
name: "epi-all-bar-incidence-counter"
description: "Count every horizontal case episode appearing in a calendar year as newly diagnosed annual incidence."
---

## When This Skill Applies
Use ONLY when every episode in a registry chart starts strictly inside the reporting year with no carry-over prevalent cases.

## Procedure
1. Count total horizontal bars as annual incidence.
2. Set `CASE_SPLIT_METHOD: TOTAL_BARS_AS_INCIDENCE`.
3. Return a JSON object with `CASE_SPLIT_METHOD` and `annual_incidence_count`.
