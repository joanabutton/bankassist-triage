# BankAssist Triage

BankAssist Triage classifies incoming digital-banking support messages and routes them to the appropriate support queue. Requests with low confidence are escalated to a human reviewer.

## Group

Group 1: Chetan Bissessur · Cristiana Lavrador · Duarte Queirós · Joana Button · Liliana Gomes
Module Machine Learning and Operation, Executive Masters in Business Analytics and AI, Porto Business School, 2026

## Project goal

Train, evaluate, register, and serve a text classifier for the ten intents in the Cleanlab banking-intent-classification dataset. The project demonstrates a complete MLOps lifecycle with MLflow: experiment tracking, model registry, promotion through `@candidate` and `@champion`, and a served API.


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
