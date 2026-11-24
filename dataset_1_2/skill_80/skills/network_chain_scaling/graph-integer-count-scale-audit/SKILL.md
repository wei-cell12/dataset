---
name: "graph-integer-count-scale-audit"
description: "Extract integer count scaling curves whose y-axis uses dot thousands separators (e.g., hundreds climbing into dot-formatted thousands)."
---

## When This Skill Applies
Use when y-axis tick marks climb monotonically from hundreds into dot-formatted thousands representing integer counts.
## Procedure
1. Parse dot-thousands tick labels as integer counts rather than small decimals.
2. Compare plotted algorithms across the x-axis range.
3. Emit compact JSON with `AXIS_SCALE_TAG: INTEGER_THOUSANDS_DOT`.
