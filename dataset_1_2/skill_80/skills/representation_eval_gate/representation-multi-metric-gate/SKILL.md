---
name: "representation-multi-metric-gate"
description: "Audit a candidate representation method across both classification accuracy (Acc) and structural metrics (AMI, Hausdorff, Edit)."
---

## Gate Branches
1. `ALL_METRIC_WINNER`: Applies ONLY when the candidate ranks first or competitive top-tier on Acc AND on structural metrics (`AMI`, `Hausdorff`, `Edit`). Sets `approved_as_all_metric_winner: true`.
2. `SINGLE_METRIC_FAIL_STRUCTURAL`: Applies whenever the candidate leads `Acc` but trails competing methods (`Concept`, `Setref`) sharply on structural metrics (`AMI`, `Hausdorff`, `Edit`). Sets `approved_as_all_metric_winner: false`.
## Output Format
Return JSON with `candidate_method`, `leads_acc`, `structural_leaders`, `gate_branch`, `approved_as_all_metric_winner`, and `rationale`.
