---
name: "ecg-12lead-st-screen"
description: "Screen complete 12-lead surface ECGs for territorial ST-segment criteria and emit triage JSON."
---

## When This Skill Applies
Use for complete, labeled 12-lead surface ECGs (`I, II, III, aVR, aVL, aVF, V1-V6`) with visible voltage calibration pulse (`10 mm/mV`).

## Preconditions
- All 12 standard leads are present and clearly labeled with a calibration pulse.
- If incomplete or unlabeled, emit `status: "INAPPLICABLE_INCOMPLETE_LEADS"`.

## Procedure
1. Confirm all 12 labeled leads and gain pulse, then map ST deviations by territory.
