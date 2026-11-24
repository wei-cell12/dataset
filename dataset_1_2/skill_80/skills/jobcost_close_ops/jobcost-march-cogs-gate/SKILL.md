---
name: "jobcost-march-cogs-gate"
description: "Audit a job-order cost schedule to determine whether a specified job should be recognized in March Cost of Goods Sold (COGS) or held in inventory."
---

## When This Skill Applies
Use to classify a specified job from a monthly job-order cost schedule (`January`, `February`, `March`, `Completed`, `Sold`) for the March 31 monthly close.
## Gate Branches
1. `RECOGNIZE_MARCH_COGS`: Applies ONLY when `sold_status == "March"`. Sets `recognize_in_march_cogs: true` and `march_cogs_usd` to the job's total accumulated cost.
2. `HOLD_FINISHED_GOODS_INVENTORY`: Applies when completed in Jan–Mar and `sold_status == "Not sold"`. Sets `recognize_in_march_cogs: false`, `march_cogs_usd: 0`.
3. `HOLD_WIP_INVENTORY`: Applies when completed after March and `sold_status == "Not sold"`.
4. `PRIOR_PERIOD_COGS_EXCLUDE`: Applies when sold in January or February.
## Output Format
Return JSON with `job_id`, `accumulated_cost_usd`, `completed_month`, `sold_status`, `gate_branch`, `recognize_in_march_cogs`, `march_cogs_usd`, and `rationale`.
