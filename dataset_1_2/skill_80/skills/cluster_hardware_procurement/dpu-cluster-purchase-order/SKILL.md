---
name: "dpu-cluster-purchase-order"
description: "Generate DPU cluster purchase-order authorization JSON from hardware scaling plots."
---

## When This Skill Applies
Use when `(tflops_with_dpu - tflops_without_dpu) / tflops_without_dpu * 100 >= 20.0` at the specified target model size.
## Procedure
1. Read TFLOPS without and with DPU at the target size and compute percent speedup.
2. Emit JSON with `target_model_size`, `target_speedup_pct`, `status: "APPROVED_DPU_PO"`, `purchase_order_allowed: true`, and `rationale`.
