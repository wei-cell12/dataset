---
name: "raw-local-attack-rate-publish"
description: "Generate local secondary attack-rate publication JSON from contact-tracing tables."
---

## When This Skill Applies
Use ONLY when the evaluated city or scope has NO footnote symbols indicating imported/reclassified cases in the local-case column.
## Procedure
1. Compute `local_cases / susceptible_contacts` directly from the printed row.
2. Emit JSON with `status: PUBLISHED_CLEAN_LOCAL_RATE` and `direct_publish_allowed: true`.
