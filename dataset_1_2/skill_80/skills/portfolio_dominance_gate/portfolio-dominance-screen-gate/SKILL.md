---
name: "portfolio-dominance-screen-gate"
description: "Screen a candidate standalone stock against mean-variance dominance across a risk-return table."
---

## Gate Branches
1. `APPROVE_GROWTH_ALLOCATION`: Applies ONLY when candidate Expected Return >= 12% AND NO other single asset in the table offers BOTH strictly higher Expected Return AND strictly lower Standard Deviation. Sets `approved_for_allocation: true`.
2. `REJECT_DOMINATED_ASSET`: Applies whenever another single asset offers strictly higher Expected Return with strictly lower Standard Deviation. Sets `approved_for_allocation: false` and `dominating_asset: <name>`.
## Output Format
Return JSON with `candidate_asset`, `expected_return_pct`, `std_dev_pct`, `dominating_asset`, `gate_branch`, `approved_for_allocation`, and `rationale`.
