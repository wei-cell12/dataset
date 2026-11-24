---
name: "corporate-liquidity-credit-gate"
description: "Audit a borrower's short-term liquidity using both Current Ratio and Quick Ratio thresholds."
---

## Gate Branches
1. `APPROVE_CREDIT_LINE`: Applies ONLY when `current_ratio >= 1.0` AND `quick_ratio >= 0.80` (where `quick_ratio = (Cash + AR) / Current Liabilities`, strictly excluding Inventory). Sets `credit_approved: true`.
2. `DECLINE_INVENTORY_ILLIQUID`: Applies whenever `current_ratio >= 1.0` but `quick_ratio < 0.80` due to heavy inventory concentration. Sets `credit_approved: false`.
3. `DECLINE_CURRENT_DEFICIT`: Applies when `current_ratio < 1.0`.
## Output Format
Return JSON with `current_ratio`, `quick_ratio`, `inventory_share_of_ca_pct`, `gate_branch`, `credit_approved`, and `rationale`.
