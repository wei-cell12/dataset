---
name: "survey-4level-likert-net-audit"
description: "Audit multi-level intensity Likert stacked polling charts to verify NET totals and category splits."
---

## When This Skill Applies
Use for public-opinion stacked bar charts presenting 4 intensity categories (`Very bad`, `Somewhat bad`, `Somewhat good`, `Very good`) alongside `NET` columns.

## Procedure
1. Record all four intensity percentages and both `NET` totals for every evaluated institution.
2. Check whether `Very + Somewhat` equals the printed `NET` (flagging any 1-point rounding difference) and compute the implicit non-response share (`100 - NET_bad - NET_good`).
3. Set `SCALE_TYPE: FOUR_LEVEL_LIKERT_NET`.
4. Emit a concise audit summary JSON containing `SCALE_TYPE`, `institutions`, `rounding_notes`, and `omitted_no_answer_pct`.
