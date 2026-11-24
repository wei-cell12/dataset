---
name: "fx-cip-low-rate-premium-audit"
description: "Audit Covered Interest Parity where the lower-interest-rate currency trades at a forward premium relative to spot."
---

## When This Skill Applies
Use when the foreign currency carries a lower interest rate than the domestic currency, pricing the foreign currency stronger in forward terms.
## Procedure
1. Compute the theoretical CIP forward rate from printed spot and interest rates and compare against the printed futures quote.
2. Emit JSON with `PARITY_TAG: LOW_RATE_CURRENCY_FORWARD_PREMIUM`.
