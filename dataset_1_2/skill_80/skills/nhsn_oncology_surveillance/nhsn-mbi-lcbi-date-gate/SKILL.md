---
name: "nhsn-mbi-lcbi-date-gate"
description: "Apply NHSN Date-of-Event and MBI-LCBI neutropenia criteria to an oncology bloodstream-infection timeline to emit surveillance reporting JSON."
---

## When This Skill Applies
Use to assign the NHSN Date of Event (DOE) and MBI-LCBI vs. Standard CLABSI category for an oncology inpatient timeline.
## Extracted Evidence
Read chronologically from the timeline:
- `admission_date`: oncology admission date
- `port_access_date`: date central line or port was accessed
- `first_positive_blood_culture_date`: date first positive diagnostic blood culture was drawn
- `organism`: identified blood culture pathogen
- `neutropenia_documented`: boolean (`true` if `ANC < 500` or `WBC <= 500` is documented within +/-3 calendar days of `first_positive_blood_culture_date`)
## Surveillance Gate Branches
1. `DOE_CULTURE_DATE_MBI_LCBI`: Applies when Date of Event is set strictly to `first_positive_blood_culture_date` (NOT port-access date), the pathogen is an eligible intestinal/MBI organism, AND `neutropenia_documented == true`. Sets `mbi_lcbi_qualified: true`.
2. `DOE_PORT_ACCESS_STANDARD_CLABSI`: Applies ONLY if diagnostic positive blood culture occurred on the port-access date without MBI neutropenia. Sets `mbi_lcbi_qualified: false`.
3. `DOE_CULTURE_DATE_STANDARD_CLABSI`: Applies when Date of Event is `first_positive_blood_culture_date` and NO neutropenia is documented around the event window. Sets `mbi_lcbi_qualified: false`.
## Output Format
Return JSON with `date_of_event`, `organism`, `neutropenia_documented`, `mbi_lcbi_qualified`, `gate_branch`, and `rationale`.
