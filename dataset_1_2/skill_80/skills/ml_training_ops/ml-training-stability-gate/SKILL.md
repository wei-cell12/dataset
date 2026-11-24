---
name: "ml-training-stability-gate"
description: "Run pre-promotion training-curve stability and collapse QA gating for ML evaluation plots."
---

## When This Skill Applies
Use when the evaluated candidate model curve exhibits early adversarial collapse (~0% for >= 10 epochs) OR an abrupt mid-training natural-accuracy drop (>= 15 percentage points), requiring a stability hold.
## Procedure
1. Verify collapse/crash window and terminal natural/adversarial accuracies for the evaluated candidate.
2. Emit JSON with `candidate_model`, `status: "HOLD_STABILITY_REVIEW"`, `auto_promote_allowed: false`, `early_adversarial_collapse: true`, and `rationale`.
