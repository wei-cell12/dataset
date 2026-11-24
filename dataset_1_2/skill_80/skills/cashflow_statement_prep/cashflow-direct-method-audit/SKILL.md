---
name: "cashflow-direct-method-audit"
description: "Prepare Operating, Investing, and Financing cash flows using the Direct Method from explicit gross cash-collection and cash-payment line items."
---

## When This Skill Applies
Use when the source schedule lists explicit gross cash inflows and outflows (such as cash collections from customers, cash payments to suppliers, interest paid, equipment sales/purchases, dividends, and stock repurchases) without accrual Net Income or depreciation.

## Procedure
1. Classify each cash line item into Operating, Investing, or Financing under U.S. GAAP Direct Method (`Interest paid on debt` is Operating under U.S. GAAP).
2. Compute `operating_cf = 300000 - 95000 - 25000 = 180000`, `investing_cf = 72000 - 33000 = 39000`, `financing_cf = -80000 - 55000 = -135000`, and `net_change_in_cash = 84000`.
3. Set `CASHFLOW_METHOD: DIRECT_GROSS_CASH_ITEMS`.
4. Return a JSON summary with `CASHFLOW_METHOD`, `operating_cf`, `investing_cf`, `financing_cf`, and `net_change_in_cash`.
