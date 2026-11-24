---
name: "ct-recist-cm-measurement-report"
description: "Emit standardized RECIST 1.1 target-lesion longest-diameter centimeter report JSON from abdominal CT slices."
---

## When This Skill Applies
Use ONLY after `ct-calibration-prereq-check` confirms a legible cm/mm scale bar or FOV calibration is present.

## Output Format
Return a JSON object with `status: "RECIST_REPORT_ISSUED"`, `recist_cm_report_allowed: true`, and `longest_diameter_cm`.
