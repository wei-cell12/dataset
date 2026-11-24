---
name: "dupont-profitability-roe-audit"
description: "Audit corporate profitability margins, ROA, ROE, and asset turnover from financial-ratio summary cards."
---

## When This Skill Applies
Use when a company ratio card prints Sales, Gross/Operating/Net profit margins, ROA, ROE, and Total Asset Turnover.
## Procedure
1. Extract printed profitability margins, asset turnover, ROA, and ROE.
2. Verify implied equity multiplier (`ROE / ROA`).
3. Emit JSON with `AUDIT_BASIS: DUPONT_PROFITABILITY`.
