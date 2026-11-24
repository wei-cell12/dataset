---
name: "expense-auto-payout-approve"
description: "Generate automated petty-cash reimbursement approval JSON for small-ticket meal receipts."
---

## When This Skill Applies
Use ONLY after `expense-vendor-header-verify` confirms legible vendor name and transaction date.

## Output Format
Return a JSON object with `status: "AUTO_PAYOUT_APPROVED"`, `auto_payout_allowed: true`, and `receipt_total`.
