---
name: "recsys-dual-metric-gate"
description: "Compare a proposed embedding-size candidate `candidate_ne` against a specified baseline `baseline_ne` on a dual-axis AUC and Logloss panel."
---

## When This Skill Applies
Use to evaluate whether `candidate_ne` strictly dominates `baseline_ne` on BOTH plotted metrics (`AUC` higher is better; `Logloss` lower is better) on the requested dataset panel.
## Gate Branches
1. `DOMINANT_SINGLE_CHOICE`: Applies ONLY when `candidate_ne` achieves strictly higher AUC AND strictly lower Logloss than `baseline_ne` on the specified panel. Sets `approved_upgrade: true`.
2. `TRADEOFF_REVIEW_REQUIRED`: Applies whenever `candidate_ne` improves one metric relative to `baseline_ne` while worsening the other metric. Sets `approved_upgrade: false`.
3. `STRICTLY_DOMINATED_REJECT`: Applies when `candidate_ne` is worse than `baseline_ne` on both metrics. Sets `approved_upgrade: false`.
## Output Format
Return JSON with `dataset_panel`, `candidate_ne`, `baseline_ne`, `gate_branch`, `approved_upgrade`, and `rationale`.
