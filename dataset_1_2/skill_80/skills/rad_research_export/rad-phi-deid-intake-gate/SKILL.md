---
name: "rad-phi-deid-intake-gate"
description: "Screen medical radiographs for de-identification and intake metadata compliance prior to research export."
---

## When This Skill Applies
Use as the mandatory HIPAA / de-identification compliance gate before exporting any medical image to a public teaching portal or external ML benchmark.

## Compliance Checks
Inspect all four corners, margins, and image headers of the radiograph:
1. `burned_in_patient_name_or_id`: boolean (`true` if a patient name, MRN/ID number, or birth/sex tag is burned into the image border)
2. `burned_in_accession_or_timestamp`: boolean (`true` if a hospital accession number or study date/time is burned into the corners)
3. `laterality_marker_visible`: boolean (`true` if an `L` or `R` marker is visible)
4. `companion_view_missing`: boolean (`true` if header states multi-view study such as `PA AND LATERAL` while only one frontal image is attached)

## Export Disposition
- If `burned_in_patient_name_or_id == true` OR `burned_in_accession_or_timestamp == true`:
  - `status`: `"BLOCKED_PHI_DEID_REQUIRED"`
  - `export_approved`: `false`
  - `required_action`: `"Quarantine image and strip/mask all burned-in header PHI before external export"`
- Otherwise:
  - `status`: `"CLEARED_DEIDENTIFIED"`
  - `export_approved`: `true`
  - `required_action`: `"Cleared for downstream dataset export"`

## Output Format
Return a single JSON object with keys `status`, `export_approved`, `burned_in_patient_name_or_id`, `burned_in_accession_or_timestamp`, `laterality_marker_visible`, `companion_view_missing`, `detected_phi_regions`, and `required_action` (do NOT repeat raw patient names verbatim in output).
