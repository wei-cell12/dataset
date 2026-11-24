---
name: "epi-case-control-odds-ratio"
description: "Analyze 2x2 case-control contingency tables with fixed case and control group sizes to compute the exposure Odds Ratio (OR)."
---

## When This Skill Applies
Use for 2x2 epidemiologic tables sampled by disease status (e.g., equal fixed case and non-case columns such as 250 cases vs. 250 controls) where population incidence cannot be directly measured.

## Procedure
1. Extract cells `a` (exposed cases), `b` (exposed controls), `c` (unexposed cases), and `d` (unexposed controls).
2. Compute `odds_ratio = round((a * d) / (b * c), 2)`.
3. Set `MEASURE_BASIS: CASE_CONTROL_ODDS_RATIO`.
4. Return a JSON summary containing `MEASURE_BASIS`, `cells`, `odds_ratio`, and a brief note explaining why Odds Ratio (not cohort Risk Ratio) applies.
