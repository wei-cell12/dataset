---
name: "survey-mean-score-1to10-audit"
description: "Audit survey bar charts reporting mean rating scores on a numeric Likert scale (e.g., 1 to 10) rather than respondent percentages."
---

## When This Skill Applies
Use when bars report mean numeric rating scores on a bounded Likert scale.
## Procedure
1. Identify the scale bounds (min to max) printed in the title/subtitle.
2. Extract each group's mean score and compute the high-to-low spread.
3. Emit structured summary JSON tagging `METRIC_BASIS: LIKERT_MEAN_SCORE`.
