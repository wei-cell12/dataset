---
name: "radiology-laterality-qa-hold"
description: "Run pre-reporting PACS orientation and frame-integrity QA gating for axial brain MRI scans."
---

## When This Skill Applies
Required BEFORE hemisphere-specific reporting whenever `R`/`L` markers are absent or DICOM overlay text is cropped off-frame.
## Procedure
1. Inspect frame borders for cropped DICOM overlay fields and check for explicit `R`/`L` laterality markers.
2. Emit JSON with `status: "HOLD_MISSING_LATERALITY_AND_CROPPED_OVERLAY"`, `draft_report_allowed: false`, and `rationale`.
