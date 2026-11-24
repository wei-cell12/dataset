---
name: "ct-interval-prior-check"
description: "Run pre-response longitudinal pairing and baseline-completeness QA gating on CT studies."
---

## When This Skill Applies
Use as the mandatory comparison pre-check before recording interval improvement, stability, or progression from abdominal CT imagery.

## Pre-Check Items
Inspect the input image(s):
1. `visible_exam_dates`: list of distinct exam dates shown in the image(s)
2. `prior_baseline_present`: boolean (`true` ONLY if at least two distinct dated comparison slices — baseline and follow-up — are visually provided)

## Gate Disposition
- If `prior_baseline_present == false`:
  - `status`: `"HOLD_NO_PRIOR_SCAN"`
  - `interval_response_allowed`: `false`
  - `action`: `"Block interval-change classification and request matched prior baseline CT slice"`
- Otherwise:
  - `status`: `"PAIRED_SCANS_VERIFIED"`
  - `interval_response_allowed`: `true`

## Output Format
Return a single JSON object with keys `visible_exam_dates`, `prior_baseline_present`, `status`, `interval_response_allowed`, and `action`.
