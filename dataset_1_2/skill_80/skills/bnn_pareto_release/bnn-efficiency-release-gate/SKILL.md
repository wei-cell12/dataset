---
name: "bnn-efficiency-release-gate"
description: "Audit a candidate binary neural network across Top-1 accuracy vs. Parameter Bits and OPs panels to emit the release-gate JSON."
---

## When This Skill Applies
Evaluate a candidate binary network against paired Top-1 vs. Parameter Bits (Mbit) and Top-1 vs. OPs plots.
## Gate Branches
1. `FRONTIER_APPROVE`: Applies ONLY when candidate achieves Top-1 >= 71.0% AND NO other plotted model achieves strictly higher Top-1 with both fewer Parameter Bits and fewer OPs. Sets `approved_for_release: true`.
2. `DOMINATED_HOLD`: Applies whenever another plotted model achieves strictly higher Top-1 accuracy at both fewer Parameter Bits and fewer OPs, even if candidate meets Top-1 >= 71.0%. Sets `approved_for_release: false` and `dominating_model: <name>`.
3. `ACCURACY_FAIL`: Applies when Top-1 < 71.0%.
## Output Format
Return JSON with `candidate_model`, `candidate_top1_approx`, `dominating_model`, `gate_branch`, `approved_for_release`, and `rationale`.
