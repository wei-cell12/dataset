---
name: "cohort-unweighted-share-average"
description: "Compute equal-weighted summary averages across demographic or legislative subgroup percentage charts."
---

## When This Skill Applies
Use when subgroup composition bars omit sample sizes `N` and must be averaged with equal subgroup weight.

## Procedure
1. Average the printed subgroup percentages equally across all listed factions.
2. Set `WEIGHTING_BASIS: EQUAL_WEIGHT_UNWEIGHTED_AVG`.
3. Return a JSON brief with `WEIGHTING_BASIS` and `unweighted_mean_pct`.
