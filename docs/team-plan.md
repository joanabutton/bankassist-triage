# Team Plan

## Presentation sequence

Each member presents for approximately one minute.

1. Duarte: business problem and BankAssist Triage solution.
2. Liliana: dataset, intent labels, splits, and evaluation approach.
3. Cristiana: classifier pipeline and model-comparison results.
4. Joana: MLflow experiments, registry, and `@champion` promotion.
5. Chetan: API and end-to-end prediction demonstration.

## Shared API contract

`POST /predict`

```json
{"query": "I need to cancel a transfer"}
```

```json
{
  "intent": "cancel_transfer",
  "confidence": 0.91,
  "route": "payments_and_transfers",
  "requires_human_review": false
}
```

## Working agreement

- Each owner creates the technical content for their own presentation section.
- Duarte integrates the final slide deck; this is not a requirement for Duarte to create every slide.
- Changes are made in feature branches and merged through pull requests after one teammate reviews them.
- `main` must remain runnable for the final demo.
