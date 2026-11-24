---
name: "recsys-hyperparam-tuning-gate"
description: "Evaluate a proposed hyperparameter setting K against dual-metric HR@20 and NDCG@20 sensitivity curves."
---

## Gate Branches
1. `OPTIMAL_PEAK_APPROVE`: Applies ONLY when both HR@20 and NDCG@20 attain their global maximum at the proposed K. Sets `approved_setting: true`.
2. `POST_PEAK_DEGRADATION`: Applies whenever both HR@20 and NDCG@20 peak at a strictly smaller K and then decline at the proposed K. Sets `approved_setting: false` and `recommended_k: <peak K>`.
## Output Format
Return JSON with `candidate_k`, `peak_k`, `gate_branch`, `approved_setting`, `recommended_k`, and `rationale`.
