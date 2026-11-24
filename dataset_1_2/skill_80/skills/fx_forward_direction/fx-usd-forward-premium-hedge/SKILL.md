---
name: "fx-usd-forward-premium-hedge"
description: "Execute U.S. dollar forward-premium FX hedging workflows from currency quote tables."
---

## When This Skill Applies
Use when `Foreign/USD` forward exceeds spot (equivalently `USD/Foreign` forward is lower than spot).
## Procedure
1. Compute the annualized USD forward premium from the printed spot and forward quotes.
2. Emit JSON with `FX_DIRECTION: USD_FORWARD_PREMIUM`.
