---
name: "utility-highlow-cost-estimate"
description: "Run high-low mixed-cost estimation on annual production-volume and factory-utility schedules."
---

## When This Skill Applies
Use when all 12 monthly activity-volume and dollar-expense rows are cleanly populated with no missing periods or corrupted labels.
## Procedure
1. Identify the highest-activity and lowest-activity months.
2. Compute variable cost per unit (`(Cost_high - Cost_low) / (Units_high - Units_low)`) and fixed cost component.
3. Emit JSON with `status: HIGHLOW_ESTIMATE_COMPLETE` and `direct_estimation_allowed: true`.
