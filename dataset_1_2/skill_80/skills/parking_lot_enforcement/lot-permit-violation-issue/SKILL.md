---
name: "lot-permit-violation-issue"
description: "Generate parking-lot permit-violation citations and stall-by-stall license-plate logs."
---

## When This Skill Applies
Use ONLY after `lot-plate-legibility-gate` confirms legible unredacted license plates and stall/time-limit signage.

## Output Format
Return a JSON object with `status: "VIOLATIONS_ISSUED"`, `citations_allowed: true`, and `cited_vehicles`.
