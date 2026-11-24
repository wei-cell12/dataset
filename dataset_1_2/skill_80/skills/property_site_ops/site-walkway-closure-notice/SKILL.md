---
name: "site-walkway-closure-notice"
description: "Issue pedestrian-corridor closure detours and access advisories for active walkway safety perimeters."
---

## When This Skill Applies
Use when cones, barricades, or caution tape stretch across a paved pedestrian walkway, blocking foot or wheelchair passage.

## Preconditions
- The paved pedestrian path is physically obstructed or closed by barriers/tape.

## Procedure
1. Emit a tenant closure JSON object with:
   - `notice_type`: `"WALKWAY_CLOSURE_DETOUR"`
   - `walkway_blocked`: `true`
   - `ada_detour_required`: `true`
   - `affected_zone`: `"main_pedestrian_walkway"`
   - `resident_message`: concise 1-sentence closure and detour alert.
