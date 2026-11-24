---
name: "optimizer-instability-spike-check"
description: "Run pre-promotion optimizer-trajectory stability gating on learning-rate schedules."
---

## When This Skill Applies
Required BEFORE promoting any learning-rate curve that suffers an abrupt loss spike and accuracy drop during training.
## Procedure
1. Log the approximate spike iteration, loss peak, and accuracy drop observed on the plot.
2. Emit JSON with `status: HOLD_EOS_SPIKE_REVIEW` and `auto_promote_allowed: false`.
