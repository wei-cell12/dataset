---
name: "epi-prevalence-vs-incidence-timeline"
description: "Count pre-existing prevalent episodes versus newly incident episodes on individual patient disease-episode timeline charts."
---

## When This Skill Applies
Use for individual episode-timeline diagrams where horizontal bars mark disease duration across a calendar window and onset symbols distinguish newly incident cases from already-ongoing pre-existing cases.
## Procedure
1. Count bars already ongoing at the start boundary (pre-existing prevalent cases, lacking an onset marker inside the window).
2. Count bars carrying an explicit onset marker inside the calendar window (newly incident cases).
3. Emit JSON with `pre_existing_cases`, `newly_incident_cases`, `total_period_prevalent_cases`, and `METRIC_BASIS: EPISODE_TIMELINE_PREVALENCE_VS_INCIDENCE`.
