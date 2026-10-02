# Infrastructure, Model Governance and Future Bank Deployment

## 1. Purpose and Current Prototype Scope

BankAssist Triage is currently developed as a **proof-of-concept machine-learning solution for banking intent classification**.

The purpose of the prototype is to demonstrate an end-to-end ML/MLOps lifecycle in which customer messages are classified into predefined banking intents and routed to the appropriate department.

The current prototype follows the architecture:

**Dataset → Data Preparation → Train/Validation/Test Split → TF-IDF → Model Training → Model Evaluation → MLflow Experiment Tracking → Model Registry → Champion Model → API → Intent Prediction**

The project is **not intended to represent a production-ready banking application**.

Enterprise cybersecurity, regulatory compliance, operational resilience and production infrastructure requirements are therefore presented as **future deployment requirements** rather than controls already implemented in the prototype.

---

# 2. Current Prototype Architecture

The prototype architecture can be represented as:

```text
Customer Message
       ↓
Prototype API
       ↓
TF-IDF Transformation
       ↓
Champion Model
       ↓
Predicted Banking Intent
       ↓
Department Routing
```

The current implementation focuses on demonstrating:

- data preparation and quality assessment;
- machine-learning model development;
- model evaluation and comparison;
- experiment tracking;
- model versioning;
- model governance;
- Champion model selection;
- API-based prediction.

---

# 3. Data Governance

Data governance begins with the quality of the dataset used to develop the classifier.

The prototype applies a defined review methodology.

### Ambiguous examples

If an observation is ambiguous but still reasonably represents one of the selected banking intents, it may remain in the dataset.

### Mislabeled examples

If an observation is clearly mislabeled but its correct intent belongs to one of the supported classes, the observation may be relabeled.

### Out-of-Scope examples

Valid banking messages whose true intent falls outside the selected classes should be excluded from model training and identified as **Out-of-Scope (OOS)**.

### Corrupted or Irrelevant examples

Nonsensical, corrupted or irrelevant observations should also be excluded, with the exclusion reason documented separately.

The purpose is not to claim that the entire dataset has been manually validated. Instead, the project performs a targeted data-quality review appropriate to the prototype scope.

Known ambiguity and remaining labeling uncertainty are documented as limitations.

---

# 4. Dataset Separation and Leakage Prevention

The prepared dataset is separated into:

**Training → Validation → Test**

The training dataset is used for model development.

The validation dataset supports model comparison and model-selection decisions.

The test dataset is reserved for final evaluation of the selected model.

Preprocessing and feature-engineering activities should respect this separation to minimise the risk of data leakage.

---

# 5. Model Development

Customer messages are transformed using **TF-IDF feature engineering**.

Candidate traditional machine-learning classification models are then trained and compared.

The objective is not simply to identify the model with the highest accuracy but to identify a model that performs consistently across the supported banking intents.

---

# 6. Model Evaluation

Candidate models are evaluated using appropriate multi-class classification metrics.

These may include:

- Accuracy;
- Precision;
- Recall;
- F1-score;
- Macro F1;
- per-class performance;
- confusion matrix.

The confusion matrix and per-class metrics are particularly important because overall accuracy alone may hide poor performance for individual banking intents.

Model-selection decisions should therefore consider both overall and class-level performance.

---

# 7. MLflow Experiment Tracking

MLflow is used to provide **experiment traceability and reproducibility**.

For each model experiment, relevant information can be recorded, including:

- model type;
- model parameters;
- MLflow Run ID;
- preprocessing configuration;
- dataset/version used;
- evaluation metrics;
- relevant evaluation artifacts;
- date of experiment.

This creates a technical record connecting each candidate model to the experiment that produced it.

The resulting lifecycle is:

**Experiment → MLflow Run → Candidate Model → Evaluation**

---

# 8. Model Registry and Champion Model

Models that satisfy the defined evaluation criteria can be registered in the **MLflow Model Registry**.

The selected model is identified as the:

**Champion Model**

The Champion represents the model currently approved for use by the prototype API.

A newly trained model should not automatically replace the existing Champion merely because it achieves a different or higher score.

Instead, it should first be treated as a **Candidate/Challenger**.

The lifecycle becomes:

**Candidate → Evaluation → Governance Decision → Model Registry → Champion**

This provides controlled model versioning and avoids uncontrolled model replacement.

---

# 9. Model Card

The project maintains a [Model Card](model-card.md) for the selected Model A. It provides a concise reference for understanding the model's intended use, supporting evidence, limitations and safeguards. It defines the scope as academic support-message classification and suggested queue routing, and explicitly excludes credit, eligibility and customer-account decisions.

The card brings together data-review and evaluation evidence, the documented champion version and source run, deployment paths, and the promotion date. The first prototype promotion was based on the technical gate, with no named human approver recorded. Future production promotions should include explicit human approval and record the approver. It also identifies unresolved issues, including the unvalidated human-review threshold and packaged-model provenance. Detailed metrics, identifiers and operating rules are kept in the card rather than repeated here.

The Model Card complements **MLflow's technical experiment and registry records** and the **promotion decision record in [notebook 3](03_mlflow_experiments.ipynb)**, discussed in section 10. MLflow provides technical traceability; the card explains the model's use and limits; the decision record captures the evidence and reason for promotion. The card supports governance review and comparison with previous champions, while the live registry establishes the current alias and the deployment configuration determines which model the API loads.

The project team should update the card whenever the champion, dataset, review threshold, supported intents or intended use changes. Production monitoring and rollback testing remain future work.

---

# 10. Governance Decision Record

The project maintains a **promotion decision record** in section 9 of [notebook 3](03_mlflow_experiments.ipynb). The documented current local-registry decision is:

| Decision Field | Recorded Evidence |
| --- | --- |
| Decision Date | 29 September 2026 |
| Candidate | `BankAssist-Intent-Classifier` version 1, Model A |
| MLflow Run ID | `d8a6d09807e74267a643c038cb2ab659` |
| Validation Evidence | Macro F1 0.9194; accuracy 0.9189 |
| Decision | Promoted to `@champion` after passing the technical gate |
| Approval Entry | `technical gate passed`; no named human approver is recorded |
| Reason | Model A had higher validation macro F1 than Model B and passed the candidate checks and the 0.90 gate |
| Previous Champion | None |
| New Champion | Version 1 (`@champion`) |

Before promotion, notebook 3 verifies that the selected run finished and is linked to the logged model. It registers that pipeline as `@candidate`, loads it through the alias, and checks the selected model source, reproduced validation scores, all ten intent classes, one probability per intent and probabilities summing to one. Promotion requires all candidate checks to pass and validation macro F1 to be at least **0.90**. Immediately before moving `@champion`, the notebook also checks that the candidate version has not changed since validation, then verifies the resulting Champion alias.

Model selection uses validation macro F1, with Model A preferred on a tie. Both models exceeded 0.90, but Model A had the higher score. The selected model's held-out test macro F1 of 0.9674 and accuracy of 0.9664 are final reporting evidence, not inputs to model selection or threshold adjustment. The 0.90 gate is an academic project acceptance rule, not a banking safety standard.

The first promotion demonstrates technical gating, not formal independent model-risk approval. Notebook 3 states that the team will review live app results and, for future promotions, review validation evidence and approve the candidate before running the promotion cell. Future records should identify the approver, candidate run and version, decision date, validation evidence, reason, and previous and new Champion versions. The notebook currently prints the previous Champion before changing the alias; it does not automatically persist a complete approval or rollback audit record.

The three governance mechanisms therefore serve complementary purposes:

**MLflow → Technical evidence**

Records how the model was produced and how it performed.

**Model Card → Model documentation**

Explains what the model is, what it is designed to do, its performance and its limitations.

**Governance Record → Decision evidence**

Documents why a model was approved, rejected or promoted.

Together they create the governance chain:

**MLflow Run → Model Card → Governance Decision → Model Registry → Champion**

---

# 11. Model Promotion Governance

A candidate model should only replace the existing Champion after completing the agreed evaluation and governance process.

The first promotion recorded in section 10 passed the technical gate and had no previous Champion. The following is an example for a **future promotion with team approval**, not a history of versions already promoted:

```text
Champion v2
     ↓
Candidate v3
     ↓
MLflow Evaluation
     ↓
Model Card
     ↓
Governance Review
     ↓
Promotion Decision
     ↓
v3 becomes Champion
     ↓
v2 retained as Previous Champion
```

A governance record could therefore contain:

| Evidence | Example |
| --- | --- |
| Candidate | Model v3 |
| MLflow Run ID | Associated experiment |
| Evaluation | Accuracy / Macro F1 |
| Model Card | Model Card v3 |
| Decision | Promote |
| Reason | Meets agreed selection criteria |
| New Champion | v3 |
| Previous Champion | v2 |
| Decision Date | Approval date |

This provides traceability between the experiment, model documentation and promotion decision.

---

# 12. Rollback and Fail-Safe Capability

The prototype already provides part of the **governance foundation required for future model rollback**.

The governance record currently captures information such as:

- decision date;
- candidate version;
- MLflow Run ID;
- score;
- reason for the decision.

Notebook 3 checks and prints the **previous Champion version** before changing the alias. Its current promotion record explicitly records **None**, so the first local Champion has no earlier approved version to restore. For future promotions, the prior version must be saved in the decision record before the alias is changed.

For example:

**Champion v2 → Candidate v3 evaluated → v3 approved → v3 becomes Champion → v2 retained as Previous Champion**

This illustrates how a future promotion can maintain traceability to the previously approved model; it is not an existing rollback target in the current local registry.

The Model Card strengthens this capability because it allows the characteristics, performance and limitations of the current and previous Champions to be compared.

The prototype therefore establishes a foundation for:

**Model Versioning + MLflow Run ID + Model Registry + Model Card + Governance Record + Previous Champion Traceability**

Notebook 3 documents a manual rollback procedure: restore `@champion` to the recorded previous version, restart the API so it reloads the model, and repeat health and prediction checks. This is a **documented rollback procedure**, not evidence of a tested recovery. An alias change also does not update `models/champion_model.pkl`; the Model Card notes that this packaged file's source run and export procedure have not been verified.

The prototype does **not** currently claim to provide automatic production rollback or operational failover.

For a future banking deployment, this governance foundation could be extended to support:

**Monitoring → Problem Detected → Incident Assessment → Rollback Decision → Previous Approved Champion → Validation → Service Restoration**

Future production controls could include:

- authorised rollback procedures;
- automatic or controlled technical rollback;
- deployment audit logs;
- monitoring triggers;
- incident-management integration;
- tested recovery procedures;
- emergency model deactivation;
- manual routing/fallback capability.

---

# 13. Current Prototype Governance Lifecycle

Combining these elements, the current governance lifecycle is:

```text
DATASET
   ↓
Data Quality Review
   ↓
Train / Validation / Test
   ↓
TF-IDF
   ↓
Model Development
   ↓
MLflow Experiment
   ↓
Candidate Model
   ↓
Model Evaluation
   ↓
Model Card
   ↓
Governance Decision
   ↓
MLflow Model Registry
   ↓
Champion
   ↓
Prototype API
   ↓
Intent Prediction
```

This allows the prototype to demonstrate:

**Traceability + Reproducibility + Documentation + Model Versioning + Controlled Promotion + Rollback Traceability**

without claiming to implement the complete control environment required by a regulated financial institution.

---

# 14. Current Prototype Limitations

The current academic prototype does not claim to provide a complete implementation of:

- enterprise Identity and Access Management;
- production Role-Based Access Control;
- bank network segregation;
- production encryption/key management;
- enterprise secrets management;
- SOC/SIEM integration;
- penetration testing;
- enterprise vulnerability management;
- formal independent model-risk validation;
- production data-protection controls;
- regulatory incident reporting;
- disaster recovery;
- business continuity;
- formal EU AI Act assessment or conformity procedures;
- DORA operational-resilience controls;
- enterprise third-party risk management;
- automatic production rollback.

These controls are outside the scope of the current prototype.

However, they would need to be assessed before deployment in a real banking environment.

---

# 15. Future Bank Production Deployment

If BankAssist were considered for deployment by a real financial institution, the prototype would need to pass through the bank's formal technology and risk-governance processes.

A potential future lifecycle would be:

```text
                 CURRENT PROTOTYPE

Dataset
   ↓
Model Development
   ↓
MLflow
   ↓
Evaluation
   ↓
Model Card
   ↓
Governance Decision
   ↓
Model Registry
   ↓
Champion
   ↓
Prototype API


          ───── FUTURE BANK DEPLOYMENT ─────


Enterprise Architecture Review
   ↓
Data Protection Assessment
   ↓
Independent Model Risk Assessment
   ↓
EU AI Act Assessment
   ↓
IT Security Assessment
   ↓
Compliance / Legal Review
   ↓
Production Readiness Assessment
   ↓
Change Approval
   ↓
Controlled Production Deployment
   ↓
Continuous Monitoring
   ↓
Incident / Rollback Management
```

These are **future production requirements and are not claimed as implemented prototype functionality**.

---

# 16. Future IT Security Architecture

From an IT Security perspective, a future production implementation should follow principles such as:

- Security by Design;
- Privacy by Design;
- Zero Trust;
- Least Privilege;
- Defence in Depth;
- Segregation of Duties;
- Human Oversight;
- Auditability.

A possible future architecture could be:

```text
Customer
   ↓
Web / Mobile Banking
   ↓
WAF / API Gateway
   ↓
Authentication & Authorisation
   ↓
Input Validation
   ↓
BankAssist API
   ↓
Approved Champion
   ↓
Intent Prediction
   ↓
Routing System
   ↓
Bank Department
```

The ML model should not directly access sensitive core banking systems unless a separately approved business and security requirement justifies that access.

---

# 17. Future Environment Segregation

A real banking implementation should separate environments:

**Development → Test/QA → Validation → Pre-Production → Production**

Development teams should not have unrestricted access to production.

Production customer data should not be copied into development environments unless specifically authorised and appropriately protected, masked or anonymised.

Production changes should follow the bank's formal change-management process.

---

# 18. Future Identity and Access Management

Production access should follow:

**Least Privilege + Role-Based Access Control + Segregation of Duties**

Potential roles include:

| Role | Responsibility |
| --- | --- |
| Data Scientist | Develop candidate models |
| ML Engineer | Maintain ML pipeline |
| Model Validator | Independently validate model |
| IT Security | Security assessment |
| Model Risk | Model-risk oversight |
| Compliance / Legal | Regulatory assessment |
| MLOps | Controlled deployment |
| Operations | Production monitoring |
| Internal Audit | Independent assurance |

A single individual should not independently:

**Develop → Validate → Approve → Deploy**

the same production model.

---

# 19. Future Data Security

Customer messages may contain personal or confidential banking information.

A production implementation should therefore consider:

- encryption in transit;
- encryption at rest;
- approved key management;
- data minimisation;
- masking/pseudonymisation where appropriate;
- retention policies;
- deletion requirements;
- restricted dataset access;
- protection of sensitive information in logs;
- dataset lineage.

Training data should be managed according to the bank's data-classification and information-security policies.

---

# 20. Future API and Application Security

A future production API should be protected by the bank's approved security infrastructure.

Potential controls include:

**API Gateway → Authentication → Authorisation → TLS → Input Validation → Rate Limiting → Monitoring → BankAssist API**

Security testing could include:

- SAST;
- dependency scanning;
- vulnerability scanning;
- secrets scanning;
- API security testing;
- authentication/authorisation testing;
- penetration testing.

Unacceptable security vulnerabilities should block production deployment.

---

# 21. Future Docker and Container Security

The prototype uses Docker to demonstrate portability and reproducibility.

For production, additional controls could include:

- approved minimal base images;
- non-root execution;
- private container registry;
- image vulnerability scanning;
- dependency scanning;
- immutable versioned images;
- no embedded passwords/API keys;
- controlled container promotion;
- image signing where required.

The same tested artifact should ideally progress through the controlled deployment lifecycle.

---

# 22. Future Secrets Management

Passwords, certificates, API keys and tokens should not be embedded in:

- Python code;
- notebooks;
- Dockerfiles;
- Git repositories;
- MLflow parameters.

A production implementation should retrieve secrets from the bank's approved secrets-management infrastructure.

---

# 23. Future Model Validation

Before production approval, the bank would likely require independent model validation.

Validation should examine not only overall performance but also model robustness.

Potential testing could include:

- spelling errors;
- ambiguous messages;
- very short messages;
- unexpected inputs;
- out-of-scope requests;
- malformed input;
- class imbalance;
- distribution changes.

Particular attention should be paid to the **business impact of misclassification**.

For example:

```text
"Someone stole my card"
        ↓
Incorrect Intent
        ↓
Wrong Department
        ↓
Potential Delay
```

A model error therefore has both a statistical dimension and a potential operational/business impact.

---

# 24. Future Human Oversight

A production implementation should not assume that every message can safely be classified into one of the supported intents.

A potential future mechanism could be:

```text
Customer Message
       ↓
Prediction
       ↓
Confidence / OOS Assessment
       ↓
 ┌─────────────┬───────────────┐
 │             │               │
Expected    Uncertain     Out-of-Scope
 │             │               │
 ▼             ▼               ▼
Route      Clarification   Human Review
```

The appropriate confidence or fallback mechanism should be established through validation rather than selected arbitrarily.

Human operators should retain the ability to correct incorrect routing where necessary.

---

# 25. Future EU AI Act Assessment

Before production deployment, the final BankAssist system should undergo an **EU AI Act assessment based on its actual intended purpose and deployment context**.

The current prototype's intended use is:

**Customer Message → Intent Classification → Department Routing**

It is not currently intended for:

**Customer Financial Data → Creditworthiness Assessment → Credit Decision**

This distinction is important.

The prototype therefore does **not claim EU AI Act certification or formal compliance**.

Instead, the project demonstrates **EU AI Act awareness** and identifies formal regulatory assessment as part of a future deployment process.

Any material change to:

- intended purpose;
- input data;
- customer population;
- model;
- decision-making authority;
- integration with banking systems;
- level of automation;

should trigger a new regulatory and risk assessment.

---

# 26. Future Monitoring

Production deployment would require continuous monitoring.

### Model Monitoring

Potential indicators include:

- prediction distribution;
- class distribution;
- routing errors;
- out-of-scope rate;
- confidence distribution;
- model drift;
- data drift;
- operator corrections.

### Technical Monitoring

Potential indicators include:

- API availability;
- response time;
- application errors;
- infrastructure failures.

### Security Monitoring

Potential indicators include:

- unauthorised access attempts;
- abnormal request volumes;
- malformed requests;
- suspicious API behaviour;
- vulnerabilities;
- abnormal privileged activity.

---

# 27. Future Incident Management and Operational Resilience

AI-related incidents should integrate with the bank's existing incident-management framework.

A possible lifecycle would be:

**Detect → Triage → Contain → Investigate → Recover → Root Cause Analysis → Remediation**

Depending on severity, relevant stakeholders could include:

- IT Security;
- SOC;
- MLOps;
- Business Owner;
- Model Risk;
- Data Protection;
- Operational Risk;
- Compliance;
- Legal.

A future deployment should also integrate with the bank's applicable operational-resilience and DORA framework.

---

# 28. Future Third-Party Risk

A real bank would also assess external dependencies used by the solution.

These could include:

- cloud providers;
- MLflow hosting;
- Git repositories;
- container registries;
- external datasets;
- external APIs;
- AI/ML service providers.

Third-party technology should be subject to the bank's applicable procurement, security and third-party risk-management processes before production adoption.

---

# 29. Future Three Lines of Defence

A mature banking deployment could apply the **Three Lines of Defence** model.

### First Line — Business and Technology

**Business Owner + Data Science + MLOps + IT Operations**

Responsible for developing and operating the solution.

### Second Line — Risk and Control

**Information Security + Model Risk + Operational Risk + Compliance + Data Protection**

Responsible for independent oversight and challenge.

### Third Line — Internal Audit

Provides independent assurance over the effectiveness of governance and controls.

---

# 30. Prototype vs Future Production

| Governance / Technology Area | Current Prototype | Future Bank Production |
| --- | --- | --- |
| Data quality review | ✓ Implemented | Formal enterprise governance |
| Train/Validation/Test | ✓ Implemented | Controlled data pipeline |
| TF-IDF | ✓ Implemented | Validated production pipeline |
| Model comparison | ✓ Implemented | Independent validation |
| MLflow tracking | ✓ Implemented | Enterprise ML platform |
| Model Card | ✓ Documented in `notebooks/model-card.md` | Formal model documentation |
| Governance decision record | ✓ First promotion recorded in notebook 3; technical gate, no named approver | Formal approval workflow |
| Model Registry | ✓ Selected pipeline registered as `@candidate` and checked | Controlled registry |
| Champion | ✓ Current local record: version 1 at `@champion` | Formally approved Champion |
| Previous Champion tracking | Previous alias checked; first promotion records None | Persisted previous approved version and rollback target |
| API | ✓ Prototype | Secured enterprise API |
| Docker | ✓ Prototype | Hardened/scanned containers |
| IAM/RBAC | Not implemented | Enterprise IAM |
| Security testing | Not implemented | Required before deployment |
|SIEM/SOC | Not implemented | Production monitoring |
| Human oversight | Review flag implemented; human-review workflow not implemented | Operational human-review control |
| EU AI Act | Awareness | Formal assessment |
| DORA | Awareness | ICT-risk/resilience framework |
| Model monitoring | Limited | Continuous |
| Incident management | Not implemented | Bank incident process |
| Rollback | Manual procedure documented; no prior Champion or tested recovery | Tested technical/operational rollback |
| Disaster recovery | Not implemented | Production resilience |
| Third-party risk | Not implemented | Formal assessment |

---

# 31. Overall Governance Framework

The complete approach can therefore be represented as:

```text
                   CURRENT PROTOTYPE

                        DATASET
                           ↓
                   Data Governance
                           ↓
                 Train / Validation / Test
                           ↓
                         TF-IDF
                           ↓
                   Model Development
                           ↓
                     MLflow Run
                           ↓
                    Model Evaluation
                           ↓
                       Model Card
                           ↓
                  Governance Decision
                           ↓
                  MLflow Model Registry
                           ↓
                       CHAMPION
                           ↓
                    Prototype API
                           ↓
                  Intent Classification


              ═══ FUTURE BANK DEPLOYMENT ═══

                           ↓
                 Enterprise Architecture
                           ↓
                 Independent Validation
                           ↓
              Data Protection Assessment
                           ↓
                   IT Security Review
                           ↓
                  Model Risk Review
                           ↓
                 EU AI Act Assessment
                           ↓
              Compliance / Legal Review
                           ↓
                   Change Approval
                           ↓
                Production Deployment
                           ↓
              Continuous Model Monitoring
                           ↓
              Security / SOC Monitoring
                           ↓
            Incident & Rollback Management
```

---

# 32. Conclusion

BankAssist should currently be considered a **governed ML/MLOps prototype rather than a production banking application**.

The prototype demonstrates:

**Data Quality + Model Development + Evaluation + MLflow Tracking + Model Card + Governance Decision + Model Registry + Champion Management + API**

The project also establishes a **governance-supported rollback foundation** through linked model versions, MLflow Run IDs and a documented promotion decision. The first recorded promotion has no previous Champion. Future promotions must retain the prior approved version and approver in the decision record; the manual rollback procedure remains to be tested.

A future banking implementation would extend this foundation with:

**Cybersecurity + Data Protection + Independent Model Validation + Model Risk + EU AI Act Assessment + DORA + Compliance + Operational Resilience + Continuous Monitoring + Technical Rollback**

This separation demonstrates a realistic path from an **academic prototype to a bank-grade production solution** without claiming that enterprise banking controls have already been implemented.
