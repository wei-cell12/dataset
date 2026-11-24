---
name: "face-id-prod-release"
description: "Generate production release approval JSON from face-verification accuracy curves."
---

## When This Skill Applies
Use when the evaluated candidate model maintains `>= 0.75` across the entire `Q4` trajectory and achieves `>= 0.85` terminal `Q4` accuracy alongside strong `LFW` accuracy.
## Procedure
1. Record approximate terminal `q4_final_acc` and `lfw_final_acc`.
2. Emit JSON with `candidate_model`, `status: "RELEASED_TO_PROD"`, `prod_release_allowed: true`, `q4_final_acc`, and `lfw_final_acc`.
