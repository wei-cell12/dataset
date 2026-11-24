---
name: "rad-cxr-intake-routing"
description: "Assign a frontal chest radiograph to the appropriate internal PACS review queue JSON based on anatomical framing and visible medical devices or catheters."
---

## When This Skill Applies
Use to route incoming frontal chest radiographs into internal radiology QA worklists strictly from visible framing and indwelling hardware/lines (do NOT assign a clinical diagnosis).

## Inspection Fields
Examine the entire chest radiograph (including the neck, clavicles, mediastinum, and upper chest wall) and record:
- `laterality_marker_visible`: boolean (`true` if `L` or `R` marker is visible)
- `bilateral_apices_and_angles_in_frame`: boolean (`true` if both lung apices and lateral costophrenic angles are included)
- `indwelling_devices_present`: boolean (`true` if any central venous catheter/line, PICC, port, chest tube, endotracheal tube, pacemaker/ICD, or sternotomy wires appear anywhere on the radiograph)
- `visible_device_description`: concise description of any visible line/device and its general location (or `"none"`)

## Routing Branches
Assign `routing_branch` strictly from the inspection fields:
1. `STANDARD_OUTPATIENT_NO_LINES`:
   - Applies ONLY when `indwelling_devices_present == false`.
   - Sets `queue: "ROUTINE_OUTPATIENT_POOL"`, `device_tip_check_required: false`.
2. `DEVICE_LINE_VERIFICATION_QUEUE`:
   - Mandatory whenever `indwelling_devices_present == true` (regardless of clean lung framing or laterality markers).
   - Sets `queue: "PRIORITY_LINE_POSITION_AUDIT"`, `device_tip_check_required: true`.

## Output Format
Return a single JSON object with keys `laterality_marker_visible`, `bilateral_apices_and_angles_in_frame`, `indwelling_devices_present`, `visible_device_description`, `routing_branch`, `queue`, `device_tip_check_required`, and `notes` (stating that clinical disease diagnosis is not assigned).
