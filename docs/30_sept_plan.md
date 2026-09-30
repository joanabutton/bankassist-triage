# BankAssist Triage: roadmap for 30 September

## Where the project stands

| Requirement | What you already have | What still needs attention |
| --- | --- | --- |
| **Business value (15%)** | A clear use case: classify banking messages and route them to support queues. | State the business goal in measurable terms. For example: reduce time to reach the correct queue while tracking misroutes and human-review rate. Present savings as a goal, not a measured result. |
| **Technical implementation (60%)** | Fixed data splits, two models, MLflow runs and promotion workflow, a packaged champion, API and Docker files, Chetan's deployment runbook, and a team check that the app appears to work. | Capture the working live path and its model source for the presentation. Show MLflow evidence separately if serving the packaged model. Fix the reproducibility and test issues below. Agree the confidence threshold tonight and make governance explicit. |
| **Presentation (10%)** | A five-person sequence in `docs/team-plan.md`. | Rehearse one timed, five-minute story with a working demo and backup screenshots. |
| **Teamwork (15%)** | Named owners for data, modelling, MLflow, API, and business value. | Give each person a speaking part and prepare everyone to answer one business and one technical question. |

## Today’s roadmap

### 1. ✅ Capture the working demo and choose the demo path — Chetan

There are now two model-serving paths to describe accurately:

- **Render path:** the runbook says `MODEL_SOURCE=local`, so the API serves the packaged champion model. MLflow is used earlier for experiment tracking and promotion, but the deployed API does not query its registry.
- **Local Compose path:** Chetan's `cd docker` followed by `docker compose up --build -d` is a valid way to start the services and has worked for the team. In this path, `docker-compose.yml` sets `MODEL_SOURCE=mlflow`, so the API loads the registered `@champion` model. The Render path uses the packaged model.

Agree with Chetan which path will be shown live. Explain the model source honestly in the pitch; do not describe the Render app as loading MLflow directly unless that is actually configured and tested.

Chetan's new notebook provides deployment steps, and the team has checked that the app appears to work. The priority is to **repeat the successful path and record it**:

1. Record the real Render API URL and save the observed `GET /health` and `POST /predict` responses. Check that the prediction has intent, confidence, route, and review status. The notebook still contains `<RENDER_API_URL>` placeholders and no executed outputs.
2. Repeat the working Lovable frontend submission during rehearsal. Confirm it calls the public Render API, not `localhost`, and displays the backend response. Capture this as evidence for the presentation.
3. Confirm the model source for the demo. If showing Render, explain that it uses the packaged `champion_model.pkl`; open notebook 3 or the MLflow UI separately to show runs, selection, and the `@champion` alias. If showing local Compose, use Chetan's working `cd docker` and `docker compose up --build -d` sequence, and confirm that the API is loading `@champion` from that MLflow store.
4. Save screenshots or a short screen recording of the working frontend, API response, Docker deployment evidence, and MLflow run/version as backup. Record which computer and URLs will be used for the presentation.

**Done when:** the team can repeat the customer-message prediction live, Chetan can explain which model artifact the API loads, and Joana can connect it to the tracked MLflow selection. The app check is encouraging; a rehearsed, captured response makes it reliable presentation evidence.

### 2. ✅ Make the existing work reproducible — Cristiana and Joana

 Record the exact split sizes, model settings, package versions, validation results, selected run, and champion version. Notebook 3 already logs much of this. Check that the published figures can be reproduced rather than typing them into a slide.

Because the Render deployment serves `models/champion_model.pkl`, also record how that packaged file was produced from the selected model and which scikit-learn version it requires. Demonstrate the connection between the MLflow decision and the deployed artifact; a registry alias changing later will not automatically update the packaged file on Render.

**Done when:** a teammate can follow the instructions, rerun the notebooks, and explain why Model A was selected.

### 3. Explain governance in the notebooks and pitch — all owners

You do not need an elaborate new system. Add short, specific explanations where the decisions happen:

- **Notebook 1, Liliana:** how possible label errors were flagged, why a human reviewed them, and how the fixed splits avoid leakage.
- **Notebook 2, Cristiana:** per-intent performance, ambiguous messages, limits of a small ten-intent dataset, and why the test set should not guide further model selection.
- ✅ **Notebook 3, Joana:** the 0.90 validation promotion gate, who approves a new champion, how to record the previous version, and how to roll back.
- **API/demo, Chetan and Duarte:** what the current 0.50 confidence threshold does, who handles human-review cases, and the threshold the team agrees tonight. Use validation examples to discuss the trade-off between review volume and incorrect automatic routes; do not tune it on the test set or present it as calibrated for real banking operations.

In the presentation, use one sentence to connect these points: **“Reviewed labels and fixed splits support evaluation; a validation gate controls promotion; uncertain messages go to a person; and a previous version can be restored.”**

**Done when:** governance is visible in the notebooks and can be explained without claiming that this classroom model is ready for real customers.

#### Governance decisions to document

Governance is a decision process across the model lifecycle. Use evidence already in the project and state the remaining policy choices clearly:

| Decision | Existing evidence | Make explicit today |
| --- | --- | --- |
| **Can we trust the data?** | Notebook 1 documents label checks, human review, and fixed splits. | Who reviewed disputed labels, what was changed, and why the train, validation, and test sets stay separate. |
| **Is the model good enough?** | Notebook 2 reports macro F1, per-intent results, and errors. | Why macro F1 drives selection, which intents are weaker, and why the test set must not be used to keep choosing variants. |
| ✅**Who approves a new version?** | Notebook 3 has MLflow runs, `@candidate`, a 0.90 validation gate, and `@champion`. | Name the reviewer, record the approved run and version, retain the previous champion version, and explain rollback. |
| **When does a person intervene?** | The API currently uses a 0.50 confidence threshold. | Tonight, agree the confidence **threshold** (the probability cutoff, not a statistical confidence interval), who handles uncertain or unmapped messages, and why the chosen value is appropriate for the demo. Record that it is not a calibrated operational threshold. |
| **What happens after release?** | Monitoring is proposed, not implemented. | Describe how to monitor misroutes, per-intent errors, confidence, review rate, and changes in message types; state when to investigate or retrain. |

Add a short **Governance decision** Markdown section at the end of each relevant notebook stage: data review in notebook 1, model limitations in notebook 2, and approval and rollback in notebook 3. A one-page model card can consolidate these decisions, but it does not replace explaining them in the notebooks and presentation.

**Check with Chetan before the demo:** the current routing code returns `Manual Review` for an unmapped intent, but `requires_human_review` depends only on confidence. The route and flag should agree when the team demonstrates human oversight.

**Suggested 30–40 second pitch wording:** “We review questionable labels before training, compare models on a fixed validation set, and promote a registered version only after its checks pass. Low-confidence requests go to human review. We retain the previous model version for rollback and would monitor misroutes and review rates before any real use.”

### 4. Fix the small demo and test inconsistencies — relevant owners

The API accepts `{"message": "..."}`, while the example in `docs/team-plan.md` uses `query`. Agree on `message` for the demo. The prediction test expects `destination`, but the API returns `route`; that test needs correction. The test environment may also need `httpx` for FastAPI’s test client. Run the tests after Chetan’s integration, and document the exact command that works. Notebook 4's terminal examples are written mainly for a Unix shell, so use commands appropriate to the demo computer.

**Done when:** the example request, API response, and tests all describe the same contract.

### 5. Rehearse the five-minute pitch — everyone

A workable allocation is:

- **Duarte, 45 seconds:** problem, proposed value, and how a pilot would measure it.
- **Liliana, 45 seconds:** reviewed data and fixed splits.
- **Cristiana, 55 seconds:** the two model results and selection metric.
- **Joana, 60 seconds:** MLflow tracking, gate, champion, and rollback.
- **Chetan, 75 seconds:** live Lovable/Render prediction or local Docker/API prediction, the model source, and the human-review rule.
- **Final 20 seconds:** limitations, governance, and conclusion.

Have each person prepare a concise answer to both “How does this help the bank?” and “How do you know this result is trustworthy?”

## Additions if the essential path is stable

In this order:

1. **Model card:** a short page with purpose, data, results, intended use, limitations, human oversight, and owners. This strengthens governance.
2. **One additional model or retraining run:** compare it on the **validation** set, log it in MLflow, and explain whether it should replace the champion. More version numbers alone are less persuasive than a documented comparison.
3. **CI:** automate the corrected tests and a Docker build in GitHub Actions. Only claim it as working after the workflow passes on GitHub.
4. **CD:** leave this last. The rubric asks for tracking or automation, not a deployed production service. A passing CI workflow and a reproducible demo are more valuable today than an untested release pipeline.

**Priority rule for today:** verify the newly documented deployment and explain the MLflow-to-packaged-model handoff first. Add model variants and CI/CD only after the team can reliably show and explain the existing end-to-end system.

| Addition | Worth doing today? | Why |
| --- | --- | --- |
| ✅**Model card** | **Yes, after the demo works.** | A short card consolidates the intended use, results, limitations, human review, and ownership. It directly supports governance. |
| **Retrain the model** | **Yes, as a reproducibility exercise.** | Rerun the existing workflow against the MLflow server used for the demo. With the same data and settings, describe this as reproducing the result—not improving the model. |
| **More model versions** | **Only if there is time to compare them properly.** | A new registered version is useful when you can show its run, validation result, and promotion decision. Extra version numbers alone add little. |
| **CI/CD** | **CI if time; CD can wait.** | A passing test and build workflow is good automation evidence. A release or deployment pipeline adds setup and failure risk today, while your existing MLflow work already demonstrates tracking. |
