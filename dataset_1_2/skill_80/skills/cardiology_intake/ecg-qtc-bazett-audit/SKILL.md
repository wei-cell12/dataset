---
name: "ecg-qtc-bazett-audit"
description: "Measure RR and QT intervals from ECG strips to compute Bazett QTc metrics."
---

## When This Skill Applies
Use ONLY when the ECG strip displays explicit printed calibration metadata: paper speed (`mm/s`), voltage gain or calibration pulse (`mm/mV`), and lead labels.
## Preconditions
- Printed paper speed (`mm/s`) is visible.
- Printed gain (`mm/mV`) and lead identifiers are visible.
- If any required calibration parameter is absent, this skill does NOT apply (return `NONE` at selection stage rather than executing this skill).
## Procedure
1. Measure RR and QT intervals using the printed paper speed.
2. Compute `QTc = QT / sqrt(RR)`.
3. Emit structured QTc measurement JSON.
