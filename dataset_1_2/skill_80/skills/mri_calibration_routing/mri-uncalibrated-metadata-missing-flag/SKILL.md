---
name: "mri-uncalibrated-metadata-missing-flag"
description: "Run pre-extraction DICOM metadata completeness and calibration QA gating on brain MRI slices."
---

## When This Skill Applies
Use ONLY when the MRI lacks a scale bar and sequence overlay metadata.
## Procedure
1. Set `QA_STATUS: UNCALIBRATED_NO_SCALE_NO_DICOM`.
