---
name: "confusion-precision-fp-audit"
description: "Run pre-approval false-positive and off-diagonal error gating on classifier confusion matrices."
---

## When This Skill Applies
Required BEFORE class approval whenever off-diagonal false positives in the target class's predicted column reduce precision below 80%.
## Procedure
1. Compute exact row recall and column precision from the matrix cells and list major confusing source classes.
2. Emit JSON with `status: HOLD_FALSE_POSITIVE_AUDIT` and `auto_approve_allowed: false`.
