---
name: "face-id-stability-audit"
description: "Run pre-release subset-stability QA gating on face-verification benchmark trajectories."
---

## When This Skill Applies
Use when the evaluated candidate model suffers a hard-subset (`Q4`) drop below `0.75` or finishes below `0.85` on `Q4`.
## Procedure
1. Record approximate `q4_final_acc`, `lfw_final_acc`, and collapse epoch.
2. Emit JSON with `candidate_model`, `status: "HOLD_Q4_COLLAPSE"`, `prod_release_allowed: false`, and `rationale`.
