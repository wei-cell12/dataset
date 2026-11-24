---
name: "order-calorie-macro-audit"
description: "Compute meal calories, protein, and sodium into nutrition JSON from restaurant orders and food packaging."
---

## When This Skill Applies
Use when an image displays either an itemized restaurant order receipt with ordered dishes/quantities or a printed Nutrition Facts table.

## Output Format
Return a JSON object with `ordered_items`, `total_calories`, and `protein_g`.
