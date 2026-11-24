---
name: "survey-or-direct-publish"
description: "Directly publish survey-reported Odds Ratios when exposure validation confirms zero misclassification."
---

## When This Skill Applies
Use ONLY when survey exposure matches actual exposure with ~100% agreement.
## Procedure
1. Emit JSON with `status: PUBLISHED_SURVEY_OR` and `direct_publish_allowed: true`.
