---
name: "poll-discrete-wave-comparison"
description: "Compare opinion shifts across multi-wave public polling time-series charts."
---

## When This Skill Applies
Use when a polling chart plots discrete survey waves across non-consecutive years.
## Procedure
1. Record each plotted survey year and percentage without interpolating missing years.
2. Compute the net shift between earliest and latest plotted waves.
3. Emit JSON with `SERIES_TYPE: DISCRETE_SURVEY_WAVES`.
