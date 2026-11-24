---
name: "cxr-completeness-calibration-qa"
description: "Run pre-signoff study-completeness and scale-calibration QA gating on chest radiographs."
---

## When This Skill Applies
Required BEFORE two-view sign-off whenever series image counters indicate an incomplete multi-image study or measurement rulers omit numeric cm/mm unit labels.
## Procedure
1. Check series completeness counters and ruler unit markings visible in the viewer overlay.
2. Emit JSON with `status: "HOLD_MISSING_IMAGE_AND_RULER_UNITS"`, `two_view_signoff_allowed: false`, and `rationale`.
