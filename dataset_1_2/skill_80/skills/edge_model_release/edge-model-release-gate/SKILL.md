---
name: "edge-model-release-gate"
description: "Audit a candidate neural network against an accuracy-vs-latency Pareto plot to emit the edge deployment release-gate JSON."
---

## When This Skill Applies
Use to evaluate a proposed edge vision model against an Accuracy (%) vs. Time (s) scatter plot containing a drawn Pareto frontier curve and parameter-count bubble legend.

## Extracted Evidence
Inspect the plot for the proposed model and all plotted alternatives:
- `candidate_model`: name of the model proposed for approval
- `candidate_accuracy_pct`: numeric accuracy (%) read from the y-axis
- `candidate_time_sec`: approximate latency (s) read from the x-axis
- `on_pareto_frontier`: boolean (`true` ONLY if the candidate point lies directly on the drawn orange Pareto frontier curve, with no plotted model achieving equal-or-higher accuracy in strictly less time)
- `dominating_model`: name of any plotted model that achieves equal-or-higher accuracy in strictly less time (or `null` if none)

## Release Gate Branches
Assign `release_branch` strictly from the frontier check:
1. `PARETO_OPTIMAL_EDGE`:
   - Applies ONLY when `on_pareto_frontier == true` AND `candidate_time_sec <= 1.0` AND `candidate_accuracy_pct >= 90.0`.
   - Sets `approved_for_release: true`, `recommended_model: <candidate_model>`.
2. `DOMINATED_REJECT`:
   - Applies whenever `on_pareto_frontier == false` (another plotted model achieves >= accuracy in less time), even if the candidate meets the `<= 1.0 s` latency and `>= 90%` accuracy targets.
   - Sets `approved_for_release: false`, `recommended_model: <dominating_model>`.
3. `LATENCY_BUDGET_EXCEEDED`:
   - Applies when `on_pareto_frontier == true` but `candidate_time_sec > 1.0`.
   - Sets `approved_for_release: false`, `recommended_model: <fastest Pareto model with accuracy >= 90% and time <= 1.0 s>`.

## Output Format
Return a single JSON object with keys `candidate_model`, `candidate_accuracy_pct`, `candidate_time_sec`, `on_pareto_frontier`, `dominating_model`, `release_branch`, `approved_for_release`, `recommended_model`, and `rationale`.
