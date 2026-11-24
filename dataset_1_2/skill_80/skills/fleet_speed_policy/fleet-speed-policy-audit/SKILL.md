---
name: "fleet-speed-policy-audit"
description: "Determine autonomous fleet target cruise speed and enforcement policy JSON from a forward-facing roadway camera frame."
---

## When This Skill Applies
Use to configure fleet cruise-speed policy for a roadway segment based on forward-facing camera sign and corridor evidence.

## Extraction Fields
Inspect the roadway frame and record:
- `posted_limit_mph`: integer read from the posted white `SPEED LIMIT` sign
- `divided_multilane`: boolean (`true` if >= 2 lanes travel in our direction with a physical center median separating oncoming traffic)
- `enforcement_plaque`: string read from any auxiliary white or yellow plaque mounted beneath the speed limit sign (`"RADAR ENFORCED"`, `"PHOTO ENFORCED"`, `"SCHOOL ZONE"`, or `"NONE"`)

## Cruise Policy Branches
Select the policy branch strictly from the extracted fields:
1. `FLOW_BUFFER_PLUS_5`:
   - Applies when `divided_multilane == true` AND `enforcement_plaque == "NONE"`.
   - Sets `target_cruise_mph = posted_limit_mph + 5`, `enforcement_alert = false`.
2. `STRICT_POSTED_CAP`:
   - Applies when `divided_multilane == false` OR `enforcement_plaque != "NONE"` (including `RADAR ENFORCED`, `PHOTO ENFORCED`, or `SCHOOL ZONE`).
   - Sets `target_cruise_mph = posted_limit_mph`, `enforcement_alert = true` (if plaque present, else `false`).

## Output Format
Return a single JSON object with keys `posted_limit_mph`, `divided_multilane`, `enforcement_plaque`, `policy_mode`, `target_cruise_mph`, `enforcement_alert`, and `rationale`.
