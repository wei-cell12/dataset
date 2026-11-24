---
name: "cxr-full-two-view-signoff"
description: "Generate complete chest-radiograph study sign-off JSON for radiology intake workflows."
---

## When This Skill Applies
Use ONLY when all views in the series (`2/2`) and numeric ruler units are provided.
## Procedure
1. Emit JSON with `status: SIGNED_OFF_TWO_VIEW` and `two_view_signoff_allowed: true`.
