---
name: "expense-auto-reimburse-usd"
description: "Directly disburse USD employee reimbursements for complete receipts displaying legible merchant, date, and currency."
---

## When This Skill Applies
Use ONLY when merchant name, date, and currency are clearly printed.
## Procedure
1. Emit JSON with `status: AUTO_REIMBURSED` and `auto_reimburse_allowed: true`.
