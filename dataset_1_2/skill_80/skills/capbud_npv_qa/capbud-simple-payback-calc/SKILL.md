---
name: "capbud-simple-payback-calc"
description: "Compute undiscounted simple payback period and cumulative undiscounted net cash flow from project cash-flow tables."
---

## When This Skill Applies
Use when initial outlay and annual cash inflows are printed and the requested metric is simple payback period (which requires no discount rate).
## Procedure
1. Divide initial outlay by uniform annual cash inflow (or accumulate inflows year by year).
2. Compute undiscounted net cash flow.
3. Emit JSON with `METRIC_BASIS: SIMPLE_PAYBACK_UNDISCOUNTED`.
