---
name: "route-corridor-clearance-check"
description: "Screen street segments for corridor obstructions and access-clearance compliance prior to dispatch."
---

## When This Skill Applies
Use before dispatching straight-through vehicle maneuvers whenever visual confirmation of corridor passability is needed.

## Clearance Checks
Inspect the entire visible street corridor (both foreground up to the intersection and the block beyond it):
1. `intersection_control`: record visible control signage (`"ALL_WAY_STOP"`, `"TRAFFIC_SIGNAL"`, `"NONE"`).
2. `posted_speed_mph`: integer if a speed limit sign is visible (else `null`).
3. `road_closed_or_detour_sign`: boolean (`true` if a `ROAD CLOSED` / `DETOUR` barricade blocks the upcoming block).
4. `active_construction_equipment_or_worker`: boolean (`true` if cones, excavator/loader machinery, or road workers occupy the roadway ahead).

## Dispatch Decision
- If `road_closed_or_detour_sign == true` OR `active_construction_equipment_or_worker == true`:
  - `status`: `"BLOCKED_DETOUR_REQUIRED"`, `proceed_straight_allowed`: `false`, `recommended_action`: `"STOP_AND_REROUTE_AT_INTERSECTION"`.
- Otherwise:
  - `status`: `"CORRIDOR_CLEAR"`, `proceed_straight_allowed`: `true`, `recommended_action`: `"PROCEED_STRAIGHT"`.

## Output Format
Return a single JSON object with keys `status`, `proceed_straight_allowed`, `intersection_control`, `posted_speed_mph`, `road_closed_or_detour_sign`, `active_construction_equipment_or_worker`, `recommended_action`, and `evidence`.
