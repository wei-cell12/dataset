---
name: "job-cost-erp-post"
description: "Post structured job-cost ledger columns into ERP accounting JSON."
---

## When This Skill Applies
Use when every component label and total row in the evaluated job column is accurately labeled and sums cleanly.
## Procedure
1. Extract Direct Materials, Direct Labor, Manufacturing Overhead, and Total Cost for the evaluated job.
2. Emit JSON with `status: POSTED_TO_ERP` and `erp_post_allowed: true`.
