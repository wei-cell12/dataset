---
name: "nhsn-hai-bloodstream-gate"
description: "Apply objective NHSN calendar-day surveillance rules to an inpatient bloodstream-infection timeline to assign POA-vs-HAI classification JSON."
---

## When This Skill Applies
Use to classify an inpatient microbiology timeline strictly under NHSN calendar-day surveillance criteria (admission date = Hospital Day 1).

## Extracted Evidence
Read chronologically from the timeline:
- `admission_date`: calendar date of admission (Hospital Day 1)
- `line_insertion_date`: date central line / PICC was placed
- `initial_cultures_negative`: boolean (`true` if Day 1–2 blood cultures returned negative)
- `first_positive_culture_date`: date of first positive blood culture
- `hospital_day_first_positive`: integer calendar day (`first_positive_culture_date - admission_date + 1`)
- `pathogens_within_14d_rit`: list of distinct blood-culture organisms identified within the 14-day Repeat Infection Timeframe starting on `first_positive_culture_date`

## Surveillance Gate Branches
Assign `routing_branch` strictly from the NHSN calendar-day rules:
1. `POA_COMMUNITY_EXCLUDE`:
   - Applies ONLY when `first_positive_culture_date` occurs on Hospital Day 1 or Day 2 (`hospital_day_first_positive <= 2`). An admission symptom note such as "possible sepsis" with negative Day 1–2 cultures does NOT qualify as POA bloodstream infection.
   - Sets `reportable_hai: false`.
2. `HAI_CLABSI_DUAL_ORGANISM`:
   - Applies when `hospital_day_first_positive >= 3` AND central line/PICC has been in place `> 2` calendar days AND two distinct bloodstream pathogens occur within the 14-day Repeat Infection Timeframe.
   - Sets `reportable_hai: true`.
3. `HAI_CLABSI_SINGLE_ORGANISM`:
   - Applies when `hospital_day_first_positive >= 3` with central line `> 2` days and only one pathogen in the 14-day window.
   - Sets `reportable_hai: true`.

## Output Format
Return a single JSON object with keys `admission_date`, `first_positive_culture_date`, `hospital_day_first_positive`, `pathogens_within_14d_rit`, `routing_branch`, `reportable_hai`, and `rationale`.
