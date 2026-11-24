---
name: "utility-missing-month-imputation-hold"
description: "Run pre-estimation schedule-completeness and cell-integrity QA gating on annual utility schedules."
---

## When This Skill Applies
Required BEFORE cost estimation whenever any month or dollar entry is missing or redacted.
## Procedure
1. Flag incomplete periods and emit JSON with `status: HOLD_INCOMPLETE_SCHEDULE` and `direct_estimation_allowed: false`.
