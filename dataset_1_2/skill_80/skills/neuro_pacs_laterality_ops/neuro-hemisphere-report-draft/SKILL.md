---
name: "neuro-hemisphere-report-draft"
description: "Draft structured hemisphere-localized neuroradiology reports from axial brain MRI scans."
---

## When This Skill Applies
Use ONLY when `R`/`L` laterality stamps and intact DICOM headers are clearly visible.
## Procedure
1. Emit JSON with `status: REPORT_DRAFT_INITIATED` and `draft_report_allowed: true`.
