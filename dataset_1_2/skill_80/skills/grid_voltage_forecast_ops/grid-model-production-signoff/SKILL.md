---
name: "grid-model-production-signoff"
description: "Generate production dispatch approval JSON from grid voltage forecast plots."
---

## When This Skill Applies
Use ONLY when `Actual` stays fully enclosed within the calibrated uncertainty band.
## Procedure
1. Emit JSON with `status: APPROVED_FOR_DISPATCH` and `production_signoff_allowed: true`.
