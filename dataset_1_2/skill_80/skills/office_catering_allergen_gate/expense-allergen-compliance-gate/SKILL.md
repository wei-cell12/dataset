---
name: "expense-allergen-compliance-gate"
description: "Audit itemized catering receipts against strictly nut-free office event rules, flagging both whole nuts and nut-derived spreads/pastes."
---

## Gate Branches
1. `APPROVE_NUT_FREE_CATERING`: Applies ONLY when no printed line item contains nuts or nut-derived spreads/pastes (hazelnut/chocolate-hazelnut spreads, almond/marzipan, peanut, pecan, walnut, pistachio, praline, pesto). Sets `nut_free_approved: true`.
2. `FLAG_TREE_NUT_ALLERGEN`: Applies whenever any line item names nuts or a recognized tree-nut spread or paste. Sets `nut_free_approved: false` and `allergen_trigger` to the offending item/ingredient.
## Output Format
Return JSON with `line_item`, `allergen_trigger`, `gate_branch`, `nut_free_approved`, and `rationale`.
