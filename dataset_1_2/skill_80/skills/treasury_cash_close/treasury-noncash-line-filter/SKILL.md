---
name: "treasury-noncash-line-filter"
description: "Run pre-posting cash-vs-accrual line-item classification gating on treasury account schedules."
---

## When This Skill Applies
Required BEFORE computing ending cash balance whenever a transaction schedule includes non-cash accrual lines alongside cash transactions.
## Procedure
1. Classify each printed line item as `cash_inflow`, `cash_outflow`, `beginning_cash`, or `noncash_exclude`.
2. Recompute ending cash using strictly cash lines.
3. Emit JSON with `status: NONCASH_LINES_FILTERED` and `direct_unfiltered_sum_allowed: false`.
