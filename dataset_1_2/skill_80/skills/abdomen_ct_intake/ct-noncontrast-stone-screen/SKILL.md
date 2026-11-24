---
name: "ct-noncontrast-stone-screen"
description: "Audit non-contrast axial abdominopelvic CT slices for urinary stone-protocol intake compliance."
---

## When This Skill Applies
Use for non-contrast axial CT slices acquired under renal-colic / urinary stone protocols where the aorta and renal parenchyma are unenhanced.

## Preconditions
- Unenhanced (non-contrast) CT acquisition without IV vascular contrast.

## Procedure
1. Confirm unenhanced vascular density and record visible renal/ureteral level.
2. Assign `intake_protocol: "NONCONTRAST_STONE_PROTOCOL_QA"` and `stone_protocol_compatible: true`.
3. Output a concise structured CT intake QA report.
