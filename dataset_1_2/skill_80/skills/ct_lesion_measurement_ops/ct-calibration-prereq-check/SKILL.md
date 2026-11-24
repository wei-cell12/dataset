---
name: "ct-calibration-prereq-check"
description: "Run pre-measurement spatial calibration and scale-integrity QA gating on exported CT slices."
---

## When This Skill Applies
Required BEFORE quantitative RECIST sizing whenever a CT slice lacks a printed cm/mm ruler or numeric in-plane FOV.
## Procedure
1. Record visible overlay fields (slice number, W/L, acquisition date if printed) and confirm absence of an in-plane calibration scale.
2. Emit JSON with `status: HOLD_MISSING_CALIBRATION_SCALE` and `quantitative_sizing_allowed: false`.
