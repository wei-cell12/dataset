---
name: "final-epoch-flops-certify"
description: "Generate efficiency certification JSON from backprop-FLOPs training schedules."
---

## When This Skill Applies
Use ONLY when post-drop FLOPs remain flat near zero without mid-training rebounds.
## Procedure
1. Emit JSON with `status: CERTIFIED_LOW_FLOPS` and `auto_certify_allowed: true`.
