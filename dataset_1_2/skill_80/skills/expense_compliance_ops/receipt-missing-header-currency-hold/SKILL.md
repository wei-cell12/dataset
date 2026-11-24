---
name: "receipt-missing-header-currency-hold"
description: "Prerequisite compliance hold triggered when a receipt lacks a legible merchant name, transaction date, or printed currency symbol."
---

## When This Skill Applies
Required BEFORE auto-reimbursement whenever merchant header/date are blurred or no currency symbol appears.
## Procedure
1. Record legible totals and flag missing merchant name, date, and currency symbol.
2. Emit JSON with `status: HOLD_MISSING_HEADER_DATE_AND_CURRENCY` and `auto_reimburse_allowed: false`.
