---
name: "ct-dicom-zslice-header-audit"
description: "Extract z-axis slice thickness, slice position, matrix dimensions, and acquisition metadata from CT slices."
---

## When This Skill Applies
Use when a CT slice prints explicit DICOM header tags (`ST`, `SP`, matrix size, date) and the user requests a header metadata audit (without uncalibrated in-plane mm lesion sizing).
## Procedure
1. Extract exact printed `ST`, `SP`, matrix dimensions, orientation markers, and date.
2. Note explicitly whether in-plane FOV/scale bar is absent.
3. Emit JSON with `AUDIT_TAG: DICOM_ZSLICE_HEADER_EXTRACTED`.
