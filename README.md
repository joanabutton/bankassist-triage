# BankAssist Triage

BankAssist Triage classifies incoming digital-banking support messages and routes them to the appropriate support queue. Requests with low confidence are escalated to a human reviewer.

## Project goal

Train, evaluate, register, and serve a text classifier for the ten intents in the Cleanlab banking-intent-classification dataset. The project demonstrates a complete MLOps lifecycle with MLflow: experiment tracking, model registry, promotion through `@candidate` and `@champion`, and a served API.

## Team

| Member | Responsibility |
| --- | --- |
| Duarte | Business use case, routing map, presentation integration |
| Liliana | Data preparation, exploratory analysis, stratified splits, evaluation data |
| Cristiana | Text-classification models and performance comparison |
| Joana | MLflow tracking, registry, promotion gate |
| Chetan | FastAPI service, simple interface, Docker and end-to-end test |

## Product flow

```text
Customer support message -> classifier -> intent and confidence -> support route or human review
```

Example: `I sent money to the wrong account` -> `cancel_transfer` -> Payments and Transfers.

## Success criteria

- A reproducible stratified train/validation/test split.
- At least two evaluated TF-IDF plus Logistic Regression pipelines.
- MLflow runs containing dataset information, parameters, macro-F1, accuracy, a confusion matrix, and prediction samples.
- A registered model that passes a promotion gate and is assigned `@champion`.
- A FastAPI `/predict` endpoint that returns intent, confidence, route, and human-review status.

## Repository layout

```text
src/          Application, training, and MLflow code
notebooks/    Exploration and experiment notebooks
tests/        Automated tests
docs/         Team notes, routing map, and presentation assets
```

## Shared setup

Create and activate a local virtual environment, then install the shared dependencies:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt
```

The `.venv` folder is ignored by Git. Each team member should create it locally rather
than commit it. Run `deactivate` when finished.

## Five-day delivery plan

1. Define the routing map, data split, metrics, and API contract.
2. Establish and log a baseline classifier.
3. Compare model variants and integrate MLflow registry workflow.
4. Serve the champion model, test the full path, and implement low-confidence escalation.
5. Rehearse the five-minute group presentation and stabilise the demo.
