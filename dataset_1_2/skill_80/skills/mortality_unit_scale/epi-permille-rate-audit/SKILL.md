---
name: "epi-permille-rate-audit"
description: "Audit epidemiological mortality rate tables reported on a per-thousand scale and compute comparative risk metrics."
---

## When This Skill Applies
Use whenever rate cells display the per-mille symbol (`‰`, per 1,000).
## Procedure
1. Read each group's printed per-mille value and convert to percent by dividing by 10.
2. Compute Relative Risk (`exposed / unexposed`) and Attributable Risk (`exposed - unexposed`).
3. Emit JSON with `UNIT_TAG: PER_MILLE_1000`.
