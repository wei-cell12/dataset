---
name: "survey-binary-forced-choice-audit"
description: "Audit two-category approval/opinion polling bar charts and summary splits."
---

## When This Skill Applies
Use for simple two-category forced-choice polling charts with no Very/Somewhat intensity split.

## Procedure
1. Record the binary positive and negative shares for each entity.
2. Set `SCALE_TYPE: BINARY_FORCED_CHOICE`.
3. Output a JSON summary with `SCALE_TYPE` and `binary_splits`.
