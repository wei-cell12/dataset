---
name: "credit-quick-ratio-liquidity-gate"
description: "Compute Current Ratio and Quick (Acid-Test) Ratio from Cash, Accounts Receivable, Inventory, and Current Liabilities on a classified balance sheet."
---

## When This Skill Applies
Use when a company financial summary provides Current Assets (Cash, Marketable Securities, Accounts Receivable, Inventory) and Current Liabilities.

## Output Format
Return a JSON object with `current_ratio`, `quick_ratio`, and `liquidity_tier`.
