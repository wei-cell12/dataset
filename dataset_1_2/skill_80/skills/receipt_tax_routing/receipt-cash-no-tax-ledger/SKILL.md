---
name: "receipt-cash-no-tax-ledger"
description: "Book non-VAT cash dining and retail receipts into the standard corporate expense ledger."
---

## When This Skill Applies
Use when a cash receipt has no separate itemized VAT/PB1 tax line (`SUB TOTAL == GRAND TOTAL`).
## Procedure
1. Extract printed line items, grand total, currency code, cash tendered, change due, and header legibility.
2. Emit JSON with `TAX_TAG: NO_SEPARATE_TAX_LINE`.
