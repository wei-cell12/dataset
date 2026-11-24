---
name: "outbreak-footnote-case-reconcile"
description: "Run pre-publication case-classification and footnote-reconciliation gating on contact-tracing tables."
---

## When This Skill Applies
Required BEFORE publishing secondary attack rates whenever any cell in the evaluated scope carries a footnote reclassifying it as imported from outside the jurisdiction.
## Procedure
1. Separate raw listed local cases from footnote-reclassified external imports and recompute adjusted local cases and attack rate.
2. Emit JSON with `status: HOLD_FOOTNOTE_RECLASSIFICATION` and `direct_publish_allowed: false`.
