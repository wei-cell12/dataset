---
name: "compute-budget-spike-audit"
description: "Run pre-certification compute-schedule stability gating on training-FLOPs plots."
---

## When This Skill Applies
Required BEFORE compute certification whenever the evaluated schedule rebounds substantially after an initial FLOPs drop.
## Procedure
1. Identify the rebound epoch window and approximate peak FLOPs from the plot.
2. Emit JSON with `status: HOLD_MIDTRAINING_REBOUND_AUDIT` and `auto_certify_allowed: false`.
