# BankAssist Triage model card

## Purpose and intended use

BankAssist Triage classifies a short digital-banking support message into one of ten supported intents. The API uses the predicted intent to suggest a support queue and returns a confidence score and a human-review flag. This is an academic demonstration of support triage. Creditworthiness assessment, credit scoring, loan approval or rejection, credit-limit decisions, transaction approval, financial eligibility decisions and actions on customer accounts are outside its intended scope, including when human oversight is present.

## Model and data

- **Selected model:** Model A, a scikit-learn pipeline with unigram TF-IDF features and `LogisticRegression(max_iter=1000, random_state=42)`.
- **Alternative tested:** Model B used unigram and bigram TF-IDF features with the same classifier. Model A was selected by validation macro F1.
- **Input and output:** Input is a message in the `text` field. The model predicts one of ten intent labels and a probability for each label. The API reports the highest probability as `confidence`; the routing and review flag are separate API rules.
- **Data:** The Cleanlab Banking Intent Classification dataset (`Cleanlab/banking-intent-classification`, loaded through Hugging Face Datasets) contained 1,000 messages. Targeted human review covered 29 flagged messages, not the entire dataset; the [review record](../banking_intent_human_quality_reviewed_Liliana.xlsx) records 13 relabelled messages, 4 retained labels, and 12 out-of-scope or invalid messages excluded from modelling. The resulting 988 messages were saved as fixed, stratified splits: 691 train, 148 validation, and 149 test. Excluded records remain in the master data for audit.
- **Supported intents:** `apple_pay_or_google_pay`, `beneficiary_not_allowed`, `cancel_transfer`, `card_about_to_expire`, `card_payment_fee_charged`, `change_pin`, `getting_spare_card`, `lost_or_stolen_phone`, `supported_cards_and_currencies`, and `visa_or_mastercard`.

## Evaluation

Macro F1 is the primary selection metric because it gives each intent equal weight. The models were fitted on the training split and compared on the validation split. Only the selected Model A was evaluated on the held-out test split.

| Model | Validation macro F1 | Validation accuracy |
| --- | ---: | ---: |
| Model A: unigrams | 0.9194 | 0.9189 |
| Model B: unigrams and bigrams | 0.9026 | 0.9054 |

Model A achieved **0.9674 test macro F1** and **0.9664 test accuracy**, correctly classifying 144 of 149 test messages. Its lowest reported test F1 scores were 0.9091 for `beneficiary_not_allowed` and 0.9167 for `getting_spare_card`. A repeated Model A MLflow run produced matching validation metrics. These results describe this small, reviewed dataset; they do not establish performance on real customer traffic.

## Tracking, version, and deployment

Notebook 3 logs the data, parameters, metrics, confusion matrix, prediction samples, and fitted pipelines in MLflow. The selected run is registered as `@candidate`, loaded and checked, and promoted to `@champion` after candidate checks and a validation macro F1 gate of at least 0.90. The held-out test result is reported, not used to choose the model or threshold. The 0.90 gate is a project acceptance rule, not a banking safety standard.

In the **local MLflow registry state verified on 29/9/2026**, `BankAssist-Intent-Classifier` version 1 is `@champion`, linked to run `d8a6d09807e74267a643c038cb2ab659`. Registry version numbers and run IDs can differ on another computer. Local Docker Compose sets `MODEL_SOURCE=mlflow`, so its API loads `models:/BankAssist-Intent-Classifier@champion` at startup. The packaged deployment path uses `models/champion_model.pkl` when `MODEL_SOURCE=local`; a later alias change does not update that file. The packaged file's exact source run and export procedure have not been verified in this card.

**Promotion date:** 29 September 2026.

The project pins `scikit-learn==1.9.0` in `requirements.txt`. Reproduction uses the committed split CSVs and notebook 3; MLflow's local database and artifacts are not committed to Git.

## Limitations and safeguards

- The ten-label model cannot reliably identify requests outside its supported intents. Similar banking wording, short or unclear messages, and label errors can cause misrouting. One questionable validation label was flagged for human review rather than silently changed.
- The maximum predicted probability is a model score, not a validated measure of real-world correctness. The API currently sets `requires_human_review=true` when confidence is strictly below **0.20**; the team has not finalised that threshold or evaluated its effect on review volume and missed errors. The flag does not enforce a human-review workflow, and the API still returns a suggested route. High confidence does not establish that a message is within the supported scope.
- Predictions should assist support staff, with a way to review uncertain or incorrect routes. Do not use message text or predictions to automate account changes, security actions, or customer eligibility decisions.
- Future champion promotions should record the candidate run, validation evidence, approver, and previous champion version. If a later version fails, the recorded prior alias can be restored and the API restarted and checked. The current local registry has no earlier champion to restore.

## Maintenance

The project team should update this card whenever the champion, dataset, review threshold, supported intents or intended use changes. Production monitoring and rollback testing remain future work.

## Evidence

- [Data preparation and review](../notebooks/01_data_exploration.ipynb)
- [Model comparison and test evaluation](../notebooks/02_modelling.ipynb)
- [MLflow tracking and promotion](../notebooks/03_mlflow_experiments.ipynb)
- [Deployment and setup](../notebooks/04_deployment_setup.ipynb)
