---
name: "mri-multisequence-perfusion-quant"
description: "Compute DWI-ADC diffusion restriction ratios and perfusion metrics from brain MRI panels."
---

## When This Skill Applies
Use when an input displays matched multi-sequence MRI panels (specifically DWI, ADC map, and dynamic contrast perfusion series with timing labels).

## Output Format
Return a JSON object with `adc_ratio`, `perfusion_cbv`, and `sequence_panel_ids`.
