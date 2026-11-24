---
name: "epi-misclassification-bias-audit"
description: "Audit case-control exposure validation tables containing survey-vs-actual misclassification, quantifying sensitivity, specificity, and OR attenuation."
---

## When This Skill Applies
Use whenever a validation table cross-tabulates survey-reported exposure against actual exposure with off-diagonal misclassification counts.
## Procedure
1. Compute Actual OR from the true-exposure marginals and Survey OR from the survey-exposure marginals.
2. Compute survey sensitivity and specificity in cases and controls.
3. Emit JSON with `BIAS_TAG: MISCLASSIFICATION_ATTENUATION_AUDIT`.
