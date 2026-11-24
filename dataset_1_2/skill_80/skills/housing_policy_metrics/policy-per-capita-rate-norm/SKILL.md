---
name: "policy-per-capita-rate-norm"
description: "Compute per-100k per-capita incidence rates and annual rate changes from population-normalized public-sector time-series charts."
---

## When This Skill Applies
Use for public-sector time-series charts that report either per-capita rates or raw caseload counts alongside explicit population denominators in the chart.

## Preconditions
- Population denominator or explicit per-100k rate axis must appear in the figure; never insert external population figures from memory.
- If only raw headcounts appear without a population denominator, do NOT compute per-100k rates—return JSON with `status: "INSUFFICIENT_DENOMINATOR_METADATA"` and list missing fields.

## Procedure
1. Extract start-year and end-year per-100k rates (or compute from printed population denominators).
2. Output JSON with `status`, `start_rate_per_100k`, `end_rate_per_100k`, `delta_per_100k`, and `missing_metadata`.
