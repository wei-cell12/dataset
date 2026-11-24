---
name: "education-all-adult-population-weighting"
description: "Compute overall U.S. adult (ages 18+) bachelor's degree completion rate weighted by racial/ethnic group population headcounts."
---

## When This Skill Applies
Use when a chart or table provides both bachelor's completion shares for all adults (18+) and explicit population headcounts per demographic group.

## Preconditions
- Scope covers all adults (ages 18+) rather than a narrow youth age band.
- Explicit group population denominators are printed on the chart.

## Output Format
Return a JSON object with `overall_adult_rate_pct`, `weighted_groups`, and `rationale`.
