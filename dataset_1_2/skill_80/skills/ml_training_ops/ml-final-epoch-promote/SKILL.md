---
name: "ml-final-epoch-promote"
description: "Generate automated checkpoint promotion JSON from ML training and evaluation curves."
---

## When This Skill Applies
Use when the evaluated candidate model's trajectory rises smoothly across epochs without early adversarial collapse or abrupt natural-accuracy crashes.
## Procedure
1. Record the candidate model's terminal natural and adversarial accuracies from the plot.
2. Confirm absence of collapse/crash events across the trajectory.
3. Emit JSON with `candidate_model`, `status: "PROMOTED_TO_RELEASE"`, `auto_promote_allowed: true`, `final_natural_acc_pct`, and `final_adversarial_acc_pct`.
