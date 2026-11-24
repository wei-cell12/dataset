---
name: "expense-vendor-header-verify"
description: "Run pre-reimbursement vendor, date, and currency legibility QA gating on meal receipt photos."
---

## When This Skill Applies
Required BEFORE auto-payout whenever the merchant header, date, or currency code is blurred or absent.
## Procedure
1. Record legible line items and printed subtotal/tax/total.
2. Flag all missing or illegible header fields.
3. Emit JSON with `status: HOLD_MISSING_VENDOR_HEADER` and `auto_payout_allowed: false`.
