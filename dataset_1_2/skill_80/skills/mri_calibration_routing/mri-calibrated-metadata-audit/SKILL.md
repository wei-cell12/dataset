---
name: "mri-calibrated-metadata-audit"
description: "Extract DICOM acquisition overlay fields (TR, TE, matrix, laterality, scale) from brain MRI slices."
---

## When This Skill Applies
Use when an MRI displays an explicit millimeter scale bar, `R`/`L` laterality markers, and TR/TE sequence parameters.
## Procedure
1. Extract all printed acquisition parameters (TR, TE, matrix size, scale-bar length, laterality stamps, date).
2. Emit JSON with `QA_STATUS: CALIBRATED_METADATA_PRESENT`.
