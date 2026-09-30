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

**NOTE** this is just responsability assignment, we have all discussed and worked on all parts of the project.

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

## MLflow tracking for notebook 3

Start the BankAssist MLflow service from the repository root:

```powershell
docker compose up -d mlflow
```

Open the MLflow UI at `http://localhost:5001`. Notebook 3 runs in the project's
local Python environment and uses that address as its tracking URI. The SQLite
database and logged model artifacts persist in `mlflow-data/`, which is ignored
by Git. The project code belongs in Git; MLflow runs and registered models live
in this local store.

When the API joins this Compose project, it should use
`MLFLOW_TRACKING_URI=http://mlflow:5000` inside Docker and load the registered
model by its `@champion` alias. A process running directly on this computer
should use `http://localhost:5001`. These addresses reach the same service.
Other computers cannot reach this `localhost` server; use the same demo
computer or arrange a shared server for a multi-computer demonstration.

To stop the service without deleting its database or artifacts, run
`docker compose down`.

## Five-day delivery plan

1. Define the routing map, data split, metrics, and API contract.
2. Establish and log a baseline classifier.
3. Compare model variants and integrate MLflow registry workflow.
4. Serve the champion model, test the full path, and implement low-confidence escalation.
5. Rehearse the five-minute group presentation and stabilise the demo.
