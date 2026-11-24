---
name: "route-straight-eta-dispatch"
description: "Generate straight-through delivery dispatch instructions and block ETA JSON for street corridors."
---

## When This Skill Applies
Use for residential delivery blocks that have already been verified open and passable for straight-through transit.

## Preconditions
- Upcoming street segment is open and cleared for straight-through travel.

## Procedure
1. Read the visible intersection control and posted speed limit (`mph`).
2. Emit straight-through dispatch JSON with `status: "DISPATCH_STRAIGHT_CONFIRMED"`, `proceed_straight_allowed: true`, `posted_speed_mph`, `next_action: "STOP_THEN_PROCEED_STRAIGHT"`, and `estimated_block_sec`.
