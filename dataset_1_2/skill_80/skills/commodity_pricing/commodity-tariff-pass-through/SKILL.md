---
name: "commodity-tariff-pass-through"
description: "Estimate landed import cost after applying printed customs tariff percentages to FOB commodity quotes."
---

## When This Skill Applies
Use when commodity charts display both FOB quotes and explicit customs tariff rates.

## Procedure
1. Compute `landed = fob * (1 + tariff_rate)` for each item.
