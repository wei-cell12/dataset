---
name: "mfg-inventory-balance-delta-audit"
description: "Compute exact period-over-period dollar and percentage inventory changes across Raw Materials, Work in Process, and Finished Goods."
---

## When This Skill Applies
Use when Beginning and Ending inventory balances (`RM`, `WIP`, `FG`) are printed and the task requests balance-sheet inventory deltas (without computing COGM/COGS).
## Procedure
1. Compute `Ending - Beginning` dollar and percentage change for RM, WIP, FG, and Total Inventory.
2. Emit JSON with `METRIC_BASIS: INVENTORY_BALANCE_DELTAS`.
