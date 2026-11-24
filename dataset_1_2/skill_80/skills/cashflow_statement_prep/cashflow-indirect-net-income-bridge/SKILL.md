---
name: "cashflow-indirect-net-income-bridge"
description: "Prepare Operating cash flows using the Indirect Method starting from accrual Net Income plus depreciation and working-capital balance-sheet changes."
---

## When This Skill Applies
Use when accrual Net Income, non-cash depreciation/amortization, and comparative working-capital changes (A/R, Inventory, A/P) are provided.

## Procedure
1. Reconcile accrual Net Income to Operating Cash Flow.
2. Set `CASHFLOW_METHOD: INDIRECT_NET_INCOME_BRIDGE`.
3. Return a JSON summary with `CASHFLOW_METHOD` and `operating_cf`.
