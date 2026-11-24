---
name: "lot-plate-legibility-gate"
description: "Run pre-citation license-plate visibility and capture-quality QA gating on parking-lot photos."
---

## When This Skill Applies
Required BEFORE issuing automated parking citations whenever visible license plates on front-row vehicles are blurred, masked, or unreadable.
## Procedure
1. Count the parked front-row vehicles facing the camera and inspect each visible license plate for legibility.
2. If plates are blurred or illegible, emit JSON with `parked_front_row_count`, `plates_legible: false`, `status: "HOLD_ILLEGIBLE_PLATES"`, and `citation_dispatch_allowed: false`.
