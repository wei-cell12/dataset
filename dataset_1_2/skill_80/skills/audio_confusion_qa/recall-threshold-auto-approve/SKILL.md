---
name: "recall-threshold-auto-approve"
description: "Generate automated class-approval JSON from event-detector confusion matrices."
---

## When This Skill Applies
Use ONLY when both row recall >= 95% and column precision >= 80%.
## Procedure
1. Emit JSON with `status: APPROVED_CLASS_DETECTOR` and `auto_approve_allowed: true`.
