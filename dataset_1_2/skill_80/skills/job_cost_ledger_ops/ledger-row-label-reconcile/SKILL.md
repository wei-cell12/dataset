---
name: "ledger-row-label-reconcile"
description: "Run pre-posting row-label and total-line reconciliation gating on job-cost schedules."
---

## When This Skill Applies
Required BEFORE ERP posting whenever any row label in the evaluated job column is misprinted or duplicated.
## Procedure
1. Identify the mislabeled line and verify arithmetic reconciliation.
2. Emit JSON with `status: HOLD_ROW_LABEL_TYPO_RECONCILE` and `erp_post_allowed: false`.
