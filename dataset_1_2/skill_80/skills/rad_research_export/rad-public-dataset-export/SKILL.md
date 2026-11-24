---
name: "rad-public-dataset-export"
description: "Generate public benchmark metadata JSON and portal release approval for medical radiographs."
---

## When This Skill Applies
Use for medical radiographs that have already cleared HIPAA de-identification screening and are ready for external dataset publication.

## Preconditions
- Image has already been verified free of burned-in patient PHI.

## Procedure
1. Record modality (`chest_radiograph`), visible orientation marker (`L`/`R`), and any visible clinical caption.
2. Emit release JSON with `status: "APPROVED_PUBLIC_EXPORT"`, `export_approved: true`, `portal_channel: "OPEN_TEACHING_BENCHMARK"`, and `metadata_summary`.
