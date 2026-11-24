---
name: "epi-cohort-incidence-rr"
description: "Analyze prospective cohort follow-up tables with exposed and unexposed at-risk denominators to compute cumulative incidence and Relative Risk (RR)."
---

## When This Skill Applies
Use for prospective cohort tables following disease-free exposed and unexposed populations over time.

## Procedure
1. Compute cumulative incidence in exposed and unexposed cohorts and take their ratio `RR`.
2. Set `MEASURE_BASIS: COHORT_RELATIVE_RISK`.
3. Return a JSON summary with `MEASURE_BASIS` and `relative_risk`.
