---
name: "emissions-trade-footprint-audit"
description: "Audit consumption-based, trade-adjusted deforestation CO2 footprints incorporating emissions embedded in imported agricultural goods."
---

## When This Skill Applies
Use when chart titles or subtitles specify trade-adjusted or consumption-based deforestation emissions.
## Procedure
1. Extract each country's printed tonnes and the averaging period from the subtitle.
2. Set `ACCOUNTING_BASIS: TRADE_ADJUSTED_CONSUMPTION_BASIS`.
3. Return structured climate-ledger JSON.
