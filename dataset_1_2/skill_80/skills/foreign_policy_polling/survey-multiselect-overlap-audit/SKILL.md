---
name: "survey-multiselect-overlap-audit"
description: "Analyze check-all-that-apply multi-select polling charts where respondents can endorse multiple foreign partners and totals exceed 100%."
---

## When This Skill Applies
Use for multi-select polling bar charts where respondents may pick more than one answer and shares sum above 100%.

## Procedure
1. Record each endorsed partner percentage and estimate overlap excess above 100%.
2. Set `RESPONSE_STRUCTURE: MULTISELECT_OVERLAPPING`.
3. Return a JSON brief with `RESPONSE_STRUCTURE` and `endorsements`.
