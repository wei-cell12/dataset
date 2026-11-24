---
name: "ct-interval-response-tracker"
description: "Log interval lesion-size progression or treatment-response status JSON from abdominal CT studies."
---

## When This Skill Applies
Use ONLY after `ct-interval-prior-check` confirms matched baseline and follow-up scans are present.

## Output Format
Return a JSON object with `status: "INTERVAL_CHANGE_LOGGED"`, `interval_response_allowed: true`, and `response_category`.
