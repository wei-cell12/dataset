---
name: "ct-iv-contrast-portal-qa"
description: "Audit intravenous-contrast enhanced axial abdominal CT slices for vascular enhancement visibility, anatomical level, and intake QA routing."
---

## When This Skill Applies
Use for axial abdominal CT slices demonstrating bright intravascular IV contrast enhancement (e.g., hyperdense abdominal aorta and portal/hepatic vessels).

## Preconditions
- Axial abdominal CT slice shows bright intravascular contrast enhancement in the aorta/major vessels.

## Procedure
1. Document `contrast_status: "iv_contrast_present"` citing bright vascular enhancement of the abdominal aorta and portal/mesenteric vessels.
2. Record visible upper-abdominal anatomical landmarks (e.g., liver, gallbladder, upper renal poles/adrenal level, stomach/bowel gas) and confirm single-slice scope without diagnosing disease.
3. Assign `intake_protocol: "PORTAL_CONTRAST_SOFT_TISSUE_QA"` and `stone_protocol_compatible: false`.
4. Output a concise structured CT intake QA report including `contrast_status`, `anatomical_level`, `intake_protocol`, `stone_protocol_compatible`, and acquisition boundaries (no HU scale/series count).
