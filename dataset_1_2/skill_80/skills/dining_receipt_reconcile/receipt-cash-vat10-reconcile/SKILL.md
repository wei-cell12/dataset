---
name: "receipt-cash-vat10-reconcile"
description: "Reconcile cash-settled dining receipts with tax-exclusive item prices, a single 10% tax line, and cash-change return lines."
---

## When This Skill Applies
Use for cash-paid restaurant receipts displaying item subtotal, a single 10% tax line, cash tendered, and cash change (including negative-signed change lines) with no service charge or credit-card gratuity.

## Procedure
1. Extract merchant name, itemized lines, `Subtotal`, `Tax`, `Total`, `CASH`, and `Cash CHANGE`.
2. Verify `Subtotal + Tax == Total` and `CASH - Total == abs(Cash CHANGE)`.
3. Set `SETTLEMENT_TYPE: CASH_TAX10_NO_SERVICE_TIP`.
4. Return a JSON reconciliation brief with `SETTLEMENT_TYPE`, `merchant`, `subtotal`, `tax`, `total`, `cash_tendered`, and `change_returned`.
