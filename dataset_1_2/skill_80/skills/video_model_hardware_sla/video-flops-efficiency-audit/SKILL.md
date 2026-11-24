---
name: "video-flops-efficiency-audit"
description: "Compare video-recognition models on Top-1 accuracy vs. theoretical GFLOPs efficiency from accuracy-vs-GFLOPs plots."
---

## When This Skill Applies
Use when benchmark panels plot Top-1 Accuracy against theoretical GFLOPs.
## Procedure
1. Read approximate Top-1 accuracy and GFLOPs for the top-performing model on each dataset panel.
2. Explicitly note that GFLOPs measures theoretical compute rather than measured GPU wall-clock FPS.
3. Emit structured JSON with `EFFICIENCY_BASIS: THEORETICAL_GFLOPS`.
