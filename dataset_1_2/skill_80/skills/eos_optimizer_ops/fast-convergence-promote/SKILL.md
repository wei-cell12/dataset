---
name: "fast-convergence-promote"
description: "Generate fast-convergence promotion JSON from learning-rate training schedules."
---

## When This Skill Applies
Use ONLY when training loss decreases smoothly without sharp spikes.
## Procedure
1. Emit JSON with `status: PROMOTED_FAST_LR` and `auto_promote_allowed: true`.
