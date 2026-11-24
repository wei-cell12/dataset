---
name: "graph-float-density-audit"
description: "Extract normalized floating-point density curves bounded on a continuous low-magnitude decimal scale."
---

## When This Skill Applies
Use ONLY when y-axis ticks represent continuous decimal densities or probabilities.
## Procedure
1. Read floating-point y-axis values directly.
2. Emit compact JSON with `AXIS_SCALE_TAG: FLOAT_DENSITY_SCALE`.
