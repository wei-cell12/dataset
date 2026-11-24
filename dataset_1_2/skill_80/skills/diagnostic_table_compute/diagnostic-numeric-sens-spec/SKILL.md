---
name: "diagnostic-numeric-sens-spec"
description: "Compute numeric sensitivity, specificity, PPV, and NPV percentages from 2x2 diagnostic validation tables."
---

## When This Skill Applies
Use when a 2x2 clinical table contains concrete numeric integer counts for TP, FP, FN, and TN.

## Output Format
Return a JSON object with `sensitivity_pct`, `specificity_pct`, `ppv_pct`, and `npv_pct`.
