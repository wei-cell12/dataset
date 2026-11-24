---
name: "ml-confusion-matrix-audit"
description: "Compute per-class precision, recall, and worst-class error pairs from normalized confusion matrix plots."
---

## When This Skill Applies
Use for square multi-class confusion matrices.

## Procedure
1. Extract off-diagonal error maxima and emit class-error audit JSON.
