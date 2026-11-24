---
name: "pantry-macro-calorie-log"
description: "Extract serving size, total calories, and macronutrient grams into nutrition JSON from packaged food items."
---

## When This Skill Applies
Use for retail food packages where a printed Nutrition Facts panel and net weight are legible on the package.

## Preconditions
- Printed Nutrition Facts panel (serving size, calories, fat/carbs/protein grams) must be legible on the package; never guess macros visually from unlabelled contents.
- If no Nutrition Facts panel is visible, output JSON with `status: "INSUFFICIENT_LABEL_METADATA"` and list missing label fields.

## Procedure
1. Extract printed serving size, calories, total fat, carbohydrates, and protein grams.
2. Emit nutrition log JSON with `status`, `serving_size`, `calories`, `macros_g`, and `missing_metadata`.
