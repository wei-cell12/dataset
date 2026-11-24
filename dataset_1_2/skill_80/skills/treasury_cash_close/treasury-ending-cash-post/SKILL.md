---
name: "treasury-ending-cash-post"
description: "Compute and post ending cash balance JSON from treasury account schedules."
---

## When This Skill Applies
Use ONLY on pre-screened cash-only ledgers containing zero non-cash accrual entries.

## Output Format
Return a JSON object with `status: "POSTED_DIRECTLY"`, `direct_blind_post_allowed: true`, and `ending_cash_usd`.
