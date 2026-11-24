---
name: "forecast-band-breach-audit"
description: "Run pre-dispatch uncertainty-band calibration gating on time-series forecast plots."
---

## When This Skill Applies
Required BEFORE production sign-off whenever the `Actual` trace exits the shaded uncertainty interval multiple times.
## Procedure
1. Inspect whether `Actual` breaches the shaded uncertainty interval across the plotted time window and check whether numeric error metrics (RMSE/MAE) are printed.
2. Emit JSON with `status: "HOLD_INTERVAL_COVERAGE_BREACH"`, `production_signoff_allowed: false`, and `rationale`.
