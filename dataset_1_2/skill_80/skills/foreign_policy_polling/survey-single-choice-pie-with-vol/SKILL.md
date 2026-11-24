---
name: "survey-single-choice-pie-with-vol"
description: "Audit mutually exclusive single-choice opinion pie charts containing volunteered `(VOL)` and `Don't know` slices summing to 100%."
---

## When This Skill Applies
Use for single-choice polling pie charts where each respondent picks one mutually exclusive slice, including volunteered `(VOL)` options and `Don't know`.

## Procedure
1. List every slice label and percentage, explicitly distinguishing prompted choices from volunteered `(VOL)` responses and `Don't know`.
2. Verify that all slices sum to 100% and compute the margin between the top two prompted choices.
3. Set `RESPONSE_STRUCTURE: SINGLE_CHOICE_EXCLUSIVE_WITH_VOL`.
4. Return a concise JSON brief containing `RESPONSE_STRUCTURE`, `slices`, `sum_pct`, and `volunteered_share_pct`.
