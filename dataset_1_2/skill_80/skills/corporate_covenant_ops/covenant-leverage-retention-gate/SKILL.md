---
name: "covenant-leverage-retention-gate"
description: "Audit a borrower's comparative balance sheet and net income against Debt/Equity leverage and Earnings Retention covenants."
---

## Gate Branches
1. `TIER1_REINVESTMENT_PASS`: Applies ONLY when current-year `Debt / Equity <= 0.60` AND `equity_retention_ratio = (Ending Equity - Beginning Equity) / Net Income >= 0.50`. Sets `covenant_pass: true`.
2. `DIVIDEND_DRAIN_FLAG`: Applies when `Debt / Equity <= 0.60` but `equity_retention_ratio < 0.50` (indicating >50% of earnings left equity via dividends/distributions). Sets `covenant_pass: false`.
3. `LEVERAGE_BREACH_FLAG`: Applies when `Debt / Equity > 0.60`.
## Output Format
Return JSON with `debt_to_equity`, `equity_change`, `net_income`, `equity_retention_ratio`, `gate_branch`, `covenant_pass`, and `rationale`.
