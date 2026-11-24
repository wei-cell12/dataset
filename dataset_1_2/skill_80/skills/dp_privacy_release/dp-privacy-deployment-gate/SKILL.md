---
name: "dp-privacy-deployment-gate"
description: "Evaluate a candidate differentially private model configuration (`class_pair`, `epsilon`) against minimum accuracy and maximum utility-drop thresholds."
---

## Gate Branches
1. `APPROVED_STRICT_DP`: Applies ONLY when accuracy at the target epsilon is `>= 92.0%` AND the accuracy drop relative to the no-noise (`eps = inf`) baseline is `<= 6.0` percentage points. Sets `approved_for_deployment: true`.
2. `REJECT_UTILITY_DROP`: Applies whenever accuracy at the target epsilon falls below `92.0%` OR the accuracy drop from `eps = inf` exceeds `6.0` percentage points. Sets `approved_for_deployment: false`.
## Output Format
Return JSON with `class_pair`, `target_epsilon`, `baseline_acc_pct`, `target_acc_pct`, `acc_drop_pp`, `gate_branch`, `approved_for_deployment`, and `rationale`.
