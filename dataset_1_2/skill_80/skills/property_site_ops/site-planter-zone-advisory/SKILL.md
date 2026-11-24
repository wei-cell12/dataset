---
name: "site-planter-zone-advisory"
description: "Log grounds and landscaping-perimeter maintenance advisories for fenced utility or garden zones."
---

## When This Skill Applies
Use for residential/commercial property photos where orange cones, delineator posts, or yellow caution tape cordon off a landscaped mulch/plant bed alongside an unobstructed paved walkway.

## Preconditions
- The concrete pedestrian path remains open and passable around the taped landscaping area.

## Procedure
1. Confirm whether the cones/tape enclose the planting bed rather than crossing the concrete walkway.
2. Emit a tenant advisory JSON object with:
   - `notice_type`: `"PLANTER_PERIMETER_ADVISORY"`
   - `walkway_blocked`: `false`
   - `ada_detour_required`: `false`
   - `affected_zone`: `"adjacent_landscaped_planter_bed"`
   - `resident_message`: concise 1-sentence note informing residents the walkway remains open and to keep off the taped planter bed.
