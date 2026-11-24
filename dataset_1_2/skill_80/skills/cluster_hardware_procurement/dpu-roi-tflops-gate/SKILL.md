---
name: "dpu-roi-tflops-gate"
description: "Run pre-procurement ROI threshold gating on DPU hardware scaling benchmarks."
---

## When This Skill Applies
Use when `(tflops_with_dpu - tflops_without_dpu) / tflops_without_dpu * 100 < 20.0` at the specified target model size.
## Procedure
1. Read TFLOPS without and with DPU at the target size and compute percent speedup.
2. Emit JSON with `target_model_size`, `target_speedup_pct`, `status: "HOLD_BELOW_20PCT_AT_TARGET"`, `purchase_order_allowed: false`, and `rationale`.
