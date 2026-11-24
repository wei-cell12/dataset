---
name: "receipt-card-service-tip-split"
description: "Reconcile dining receipts with itemized service charges, gratuities, and payment breakdowns."
---

## When This Skill Applies
Use for credit-card restaurant receipts listing separate service charge, tip, and card-payment lines.

## Procedure
1. Split food subtotal, service charge, tip, and card fee.
2. Set `SETTLEMENT_TYPE: CARD_WITH_SERVICE_AND_TIP`.
3. Return a JSON brief with `SETTLEMENT_TYPE` and fee breakdown.
