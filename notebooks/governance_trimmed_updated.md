# Infrastructure, Model Governance and Future Bank Deployment

## 1. Purpose and Current Prototype Scope

BankAssist Triage is currently developed as a **proof-of-concept machine-learning solution for banking intent classification**.

The purpose of the prototype is to demonstrate an end-to-end ML/MLOps lifecycle in which customer messages are classified into predefined banking intents and routed to the appropriate department.

The current prototype follows the architecture:

**Dataset → Data Preparation → Train/Validation/Test Split → TF-IDF → Model Training → Model Evaluation → MLflow Experiment Tracking → Model Registry → Champion Model → API → Intent Prediction**

The project is **not intended to represent a production-ready banking application**. Enterprise cybersecurity, regulatory compliance, operational resilience and production infrastructure requirements are therefore presented as **future deployment requirements**, not as controls already implemented in the prototype.

---

## 2. Current Prototype Architecture

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

- data preparation and targeted data-quality review;
- train/validation/test separation;
- machine-learning model development and evaluation;
- MLflow experiment tracking and model versioning;
- controlled Candidate-to-Champion promotion;
- model documentation and governance records;
- API-based prediction and suggested routing.

---

## 3. Data Governance and Dataset Separation

Data governance begins with the quality of the dataset used to develop the classifier. The prototype applies a defined review methodology to **flagged observations**, rather than claiming that the full dataset has been manually validated.

### Review outcomes

- **KEEP** — the original label remains reasonable.
- **RELABEL** — the observation is valid, but another supported intent is clearly more appropriate.
- **EXCLUDE OOS** — the message is a valid banking request but falls outside the selected intents.
- **EXCLUDE INVALID** — the observation is nonsensical, corrupted, malformed or irrelevant.

Known ambiguity and remaining labelling uncertainty are documented as limitations.

### Train / validation / test separation

The prepared dataset is separated into:

**Training → Validation → Test**

- The **training** split is used for model fitting.
- The **validation** split supports model comparison and model-selection decisions.
- The **test** split is reserved for final evaluation of the selected model.

Preprocessing and feature-engineering activities should respect this separation to minimise the risk of data leakage.

---

## 4. Model Development and Evaluation

Customer messages are transformed using **TF-IDF feature engineering**, and candidate traditional machine-learning classifiers are trained and compared.

Evaluation considers more than overall accuracy. Relevant measures include:

- Accuracy;
- Precision;
- Recall;
- F1-score;
- Macro F1;
- per-class performance;
- confusion matrix.

Macro F1 is the primary model-selection metric because it gives each supported intent equal weight. The confusion matrix and per-class metrics help identify weaknesses that overall accuracy could hide.

For the current prototype, Model A achieved higher validation performance than Model B and was selected using validation evidence only. The held-out test result is used for final reporting, not for model selection or threshold tuning.

---

## 5. MLflow Tracking, Registry and Model Card

### MLflow experiment tracking

MLflow provides **experiment traceability and reproducibility**. Relevant information recorded for model experiments includes:

- model type and parameters;
- preprocessing configuration;
- dataset/version information;
- validation metrics;
- evaluation artifacts;
- MLflow Run ID;
- fitted pipeline.

This creates a technical record connecting each candidate model to the experiment that produced it.

**Experiment → MLflow Run → Candidate Model → Evaluation**

### Model Registry and Champion

Models that satisfy the defined evaluation criteria can be registered in the **MLflow Model Registry**. A new model should not automatically replace the existing Champion merely because it has a different or higher score.

The intended lifecycle is:

**Candidate → Evaluation → Governance Decision → Model Registry → Champion**

The Champion represents the model currently approved for use by the prototype API configuration.

### Model Card

The project maintains a [Model Card](model-card.md) for the selected Model A. It provides a concise reference for intended use, supporting evidence, limitations and safeguards, and explicitly excludes credit, eligibility, transaction and customer-account decisions from the prototype scope.

The card brings together data-review and evaluation evidence, the documented champion version and source run, deployment paths, and the promotion date. **The first prototype promotion was based on the technical gate, with no named human approver recorded. Future production promotions should include explicit human approval and record the approver.** It also identifies unresolved issues, including the unvalidated human-review threshold and packaged-model provenance. Detailed metrics, identifiers and operating rules are kept in the card rather than repeated here.

The Model Card complements **MLflow's technical experiment and registry records** and the **promotion decision record in [notebook 3](03_mlflow_experiments.ipynb)**:

- **MLflow → Technical evidence** — how the model was produced and how it performed.
- **Model Card → Model documentation** — intended use, performance, limitations and safeguards.
- **Governance Record → Decision evidence** — why a model was approved, rejected or promoted.

Together they form the governance chain:

**MLflow Run → Model Card → Governance Decision → Model Registry → Champion**

The card should be updated whenever the champion, dataset, review threshold, supported intents or intended use changes. Production monitoring and rollback testing remain future work.

---

## 6. Governance Decision, Promotion and Rollback

### Current promotion decision record

The project maintains a promotion decision record in notebook 3. The documented current local-registry decision is:

| Decision Field | Recorded Evidence |
| --- | --- |
| Decision Date | 29 September 2026 |
| Candidate | `BankAssist-Intent-Classifier` version 1, Model A |
| MLflow Run ID | `d8a6d09807e74267a643c038cb2ab659` |
| Validation Evidence | Macro F1 0.9194; accuracy 0.9189 |
| Decision | Promoted to `@champion` after passing the technical gate |
| Approval Entry | `technical gate passed`; no named human approver recorded |
| Reason | Model A had higher validation macro F1 than Model B and passed the candidate checks and the 0.90 gate |
| Previous Champion | None |
| New Champion | Version 1 (`@champion`) |

Before promotion, notebook 3 verifies that the selected run finished and is linked to the logged model. It registers the pipeline as `@candidate`, loads it through the alias, and checks:

- the selected model source;
- reproduced validation scores;
- all ten intent classes;
- one probability per intent;
- probabilities summing to one.

Promotion requires all candidate checks to pass and validation macro F1 to be at least **0.90**. Immediately before moving `@champion`, the notebook also checks that the candidate version has not changed since validation and then verifies the resulting Champion alias.

The selected model's held-out test macro F1 of **0.9674** and accuracy of **0.9664** are final reporting evidence, not inputs to model selection or threshold adjustment. The 0.90 gate is an academic project acceptance rule, not a banking safety standard.

### Human approval

The first promotion demonstrates **technical gating**, not formal independent model-risk approval. No named human approver was recorded for the prototype promotion. Future production promotions should require explicit human approval and retain the approver, candidate run and version, decision date, validation evidence, reason, and previous and new Champion versions.

### Rollback foundation

The prototype establishes a governance foundation for future rollback through:

**Model Versioning + MLflow Run ID + Model Registry + Model Card + Governance Record + Previous Champion Traceability**

Notebook 3 checks and prints the previous Champion before changing the alias. The first promotion records **None**, so there is currently no earlier approved Champion to restore.

For future promotions, the previous Champion should be persisted in the decision record before the alias changes. Notebook 3 documents a manual rollback procedure:

1. restore `@champion` to the recorded previous version;
2. restart the API so it reloads the model;
3. repeat health and prediction checks.

This is a **documented rollback procedure**, not evidence of tested recovery. An MLflow alias change also does not update `models/champion_model.pkl`; the Model Card notes that the packaged file's source run and export procedure have not been verified.

The prototype therefore does **not** claim automatic production rollback or operational failover.

---

## 7. Current Prototype Limitations

The current academic prototype does not claim to provide a complete implementation of:

- enterprise Identity and Access Management;
- production Role-Based Access Control;
- bank network segregation;
- production encryption and key management;
- enterprise secrets management;
- SOC/SIEM integration;
- penetration testing;
- enterprise vulnerability management;
- formal independent model-risk validation;
- production data-protection controls;
- regulatory incident reporting;
- disaster recovery and business continuity;
- formal EU AI Act assessment or conformity procedures;
- formal GDPR privacy assessment, including a DPIA where required;
- DORA operational-resilience controls;
- ISO/IEC conformity assessment or certification;
- enterprise third-party risk management;
- automatic production rollback.

These controls are outside the current prototype scope and would need to be assessed before deployment in a real banking environment.

---

## 8. Future Bank Production Requirements

If BankAssist were considered for deployment by a real financial institution, it would need to pass through the bank's formal architecture, security, risk, compliance and change-management processes.

A possible high-level lifecycle would include:

**Enterprise Architecture Review → Data Protection Assessment → Independent Model Risk Assessment → EU AI Act Assessment → IT Security Assessment → Compliance / Legal Review → Production Readiness Assessment → Change Approval → Controlled Production Deployment → Continuous Monitoring → Incident / Rollback Management**

### 8.1 Security, access and environments

A future production implementation should follow principles such as:

- Security by Design;
- Privacy by Design;
- Zero Trust;
- Least Privilege;
- Defence in Depth;
- Segregation of Duties;
- Human Oversight;
- Auditability.

Production environments should be separated from development and testing, for example:

**Development → Test/QA → Validation → Pre-Production → Production**

Development teams should not have unrestricted production access, and production customer data should not be copied into development environments unless specifically authorised and appropriately protected.

Production access should follow **Least Privilege + Role-Based Access Control + Segregation of Duties**. Potential roles include Data Science, ML Engineering, Model Validation, IT Security, Model Risk, Compliance/Legal, MLOps, Operations and Internal Audit. A single person should not independently develop, validate, approve and deploy the same production model.

### 8.2 Data, API, container and secrets security

Customer messages may contain personal or confidential banking information. A production implementation should therefore consider:

- encryption in transit and at rest;
- approved key management;
- data minimisation;
- masking or pseudonymisation where appropriate;
- retention and deletion requirements;
- restricted dataset access;
- protection of sensitive information in logs;
- dataset lineage.

A production API should sit behind approved security infrastructure and could include:

**API Gateway → Authentication → Authorisation → TLS → Input Validation → Rate Limiting → Monitoring → BankAssist API**

The BankAssist model should not directly access sensitive core-banking systems unless a separately approved business, architecture and security requirement justifies that access.

Security testing could include SAST, dependency and vulnerability scanning, secrets scanning, API security testing, authentication/authorisation testing and penetration testing. **Unacceptable security vulnerabilities should block promotion to production until they are remediated or formally risk-accepted under the bank's governance process.**

For containerised deployment, additional controls could include approved minimal base images, non-root execution, a private registry, image vulnerability scanning, immutable versioned images, image signing where required, and no embedded credentials. **Where practicable, the same immutable, tested model and container artifacts should progress through the controlled deployment lifecycle rather than being rebuilt independently for production.**

Passwords, certificates, API keys and tokens should not be embedded in source code, notebooks, Dockerfiles, Git repositories or MLflow parameters; production systems should use approved secrets-management infrastructure.

### 8.3 Model validation, robustness and human oversight

Before production approval, the bank would likely require independent model validation covering both statistical performance and business impact. Potential robustness testing includes:

- spelling errors;
- ambiguous and very short messages;
- unexpected or malformed inputs;
- out-of-scope requests;
- class imbalance;
- distribution changes.

**Bias and fairness should also be considered during validation.** For this routing use case, this would include checking whether performance, confidence and human-review rates vary systematically across relevant message characteristics or customer groups where appropriate data is available. The current prototype does not contain sufficient demographic information to claim a demographic fairness assessment.

Misclassification can cause operational harm through incorrect routing and delay, so business impact should be considered alongside model metrics.

The current prototype includes a **review flag**, but it does not implement a complete operational human-review workflow. A future mechanism could distinguish expected, uncertain and out-of-scope cases and route uncertain cases to human review or clarification.

The appropriate confidence or fallback mechanism should be established through validation rather than selected arbitrarily, and human operators should retain the ability to correct routing where necessary.

### 8.4 Legal, regulatory and standards framework

A future banking deployment would require a formal legal and regulatory assessment based on the **actual intended purpose, data processed, deployment context and level of automation**. The current prototype demonstrates awareness of these requirements but does **not** claim legal compliance, regulatory approval, conformity assessment or ISO certification.

#### EU Artificial Intelligence Act

The **EU AI Act — Regulation (EU) 2024/1689** — applies a risk-based framework to AI systems. The final regulatory treatment of BankAssist would depend on how the system is used in practice, not simply on the fact that it uses machine learning.

The current prototype's intended use is:

**Customer Message → Intent Classification → Suggested Department Routing**

It is explicitly outside the prototype scope to perform:

**Customer Financial Data → Creditworthiness / Eligibility Assessment → Financial Decision**

This distinction matters because a routing assistant and a system used to support creditworthiness or other consequential financial decisions have materially different purposes and risk implications. The project should therefore **not assign itself a definitive AI Act risk category at prototype stage**. A real deployment should document the intended purpose, identify the relevant provider/deployer roles, assess the applicable AI Act obligations and repeat that assessment whenever the purpose, model, data, customer population, integrations or degree of automation changes.

#### General Data Protection Regulation (GDPR)

The **GDPR — Regulation (EU) 2016/679** — is directly relevant because real customer-support messages may contain personal data and, in some cases, sensitive information. A production implementation would therefore need a documented privacy assessment covering at least:

- the roles and responsibilities of the data controller and any processors;
- a valid legal basis for each processing purpose;
- clear transparency information explaining what data is processed, why, for how long and by whom;
- **purpose limitation** and **data minimisation**, so only information needed for routing is processed;
- data accuracy, retention and deletion rules;
- appropriate technical and organisational security measures;
- processes for applicable data-subject rights, including access, rectification, erasure, restriction and objection;
- processor and third-party arrangements, including international-transfer safeguards where relevant;
- a **Data Protection Impact Assessment (DPIA)** where the proposed processing is likely to create a high risk to individuals' rights and freedoms.

The current BankAssist use case is designed for support routing rather than decisions that produce legal or similarly significant effects. If the system were later extended into automated eligibility, credit, account-security or other consequential decisions, the privacy and automated-decision-making assessment would need to be revisited.

#### Digital Operational Resilience Act (DORA)

The **Digital Operational Resilience Act — Regulation (EU) 2022/2554** — establishes an EU framework for managing ICT and cyber risk in the financial sector. BankAssist is not itself a financial institution, but a bank deploying it would need to assess the solution within its DORA control environment. Relevant areas would include:

- ICT risk management and security controls;
- operational resilience and service continuity;
- incident detection, classification, response and recovery;
- resilience testing;
- governance of ICT third-party dependencies, including cloud or hosted services;
- documented rollback, fallback and recovery arrangements.

This aligns with the security, monitoring, incident-management and third-party controls described elsewhere in this document.

#### Relevant ISO/IEC standards

ISO standards are **international standards rather than EU legislation**. They can support a structured governance and control environment, but using or even certifying against an ISO standard does not by itself establish compliance with the EU AI Act, GDPR or DORA.

For a future BankAssist deployment, the most relevant standards include:

| Standard | Relevance to BankAssist |
| --- | --- |
| **ISO/IEC 42001:2023** — Artificial Intelligence Management System | Organisation-wide AI governance, accountability, risk management, documented controls and continual improvement. |
| **ISO/IEC 23894:2023** — AI risk-management guidance | Structured identification, assessment, treatment and monitoring of AI-specific risks. |
| **ISO/IEC 27001:2022** — Information Security Management System | Governance of information-security risks affecting customer messages, APIs, infrastructure, access and model artifacts. |
| **ISO/IEC 27701:2025** — Privacy Information Management System | Privacy governance for organisations acting as controllers or processors of personally identifiable information; complementary to GDPR-oriented privacy management. |

These standards would be best treated as **supporting governance frameworks**. A future bank could decide whether to align with them, integrate them into existing certified management systems, or require formal certification depending on its own governance and supplier requirements.

#### Combined compliance view

The frameworks serve different but complementary purposes:

**EU AI Act → AI-system risk and governance**  
**GDPR → Personal-data protection and individual rights**  
**DORA → Financial-sector ICT and operational resilience**  
**ISO/IEC standards → Structured international management and risk-control frameworks**

A production-readiness review should assess these frameworks together rather than treating any single one as sufficient on its own.

### 8.5 Monitoring, incidents and resilience

Production deployment would require continuous monitoring across several dimensions.

**Model monitoring** could include prediction distribution, class distribution, routing errors, out-of-scope rate, confidence distribution, model drift, data drift and operator corrections.

**Technical monitoring** could include API availability, response time, application errors and infrastructure failures.

**Security monitoring** could include unauthorised access attempts, abnormal request volumes, malformed requests, suspicious API behaviour, vulnerabilities and abnormal privileged activity.

AI-related incidents should integrate with the bank's existing incident-management framework, for example:

**Detect → Triage → Contain → Investigate → Recover → Root Cause Analysis → Remediation**

Future production controls should include tested recovery procedures, authorised rollback, deployment audit logs, monitoring triggers, emergency model deactivation and manual routing/fallback capability.

### 8.6 Third-party and enterprise governance

A real bank would assess relevant external dependencies such as cloud providers, MLflow hosting, Git repositories, container registries, external datasets, external APIs and AI/ML service providers through its procurement, security and third-party risk processes.

A mature deployment could also apply the **Three Lines of Defence** model:

- **First Line — Business and Technology:** Business Owner, Data Science, MLOps and IT Operations.
- **Second Line — Risk and Control:** Information Security, Model Risk, Operational Risk, Compliance and Data Protection.
- **Third Line — Internal Audit:** independent assurance over the effectiveness of governance and controls.

---

## 9. Prototype vs Future Production

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
| SIEM/SOC | Not implemented | Production monitoring |
| Human oversight | Review flag implemented; human-review workflow not implemented | Operational human-review control |
| EU AI Act | Awareness | Formal intended-purpose and regulatory assessment |
| GDPR | Awareness; no production privacy framework claimed | Formal privacy assessment, lawful basis, transparency, minimisation, retention, rights and DPIA where required |
| DORA | Awareness | ICT-risk and operational-resilience framework |
| ISO/IEC standards | Not assessed or certified | Consider ISO/IEC 42001, 23894, 27001 and 27701 as supporting governance frameworks |
| Model monitoring | Limited | Continuous |
| Incident management | Not implemented | Bank incident process |
| Rollback | Manual procedure documented; no prior Champion or tested recovery | Tested technical/operational rollback |
| Disaster recovery | Not implemented | Production resilience |
| Third-party risk | Not implemented | Formal assessment |

---

## 10. Overall Governance Framework

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
             GDPR / Data Protection Assessment
                           ↓
                   IT Security Review
                           ↓
                  Model Risk Review
                           ↓
            EU AI Act / Regulatory Assessment
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

## 11. Conclusion

BankAssist should currently be considered a **governed ML/MLOps prototype rather than a production banking application**.

The prototype demonstrates:

**Data Quality + Model Development + Evaluation + MLflow Tracking + Model Card + Governance Decision + Model Registry + Champion Management + API**

It also establishes a governance-supported rollback foundation through linked model versions, MLflow Run IDs and a documented promotion decision. The first recorded promotion has no previous Champion and no named human approver. Future promotions should retain the prior approved version and explicit approver in the decision record; the manual rollback procedure remains to be tested.

A future banking implementation would extend this foundation with:

**Cybersecurity + GDPR/Data Protection + Independent Model Validation + Model Risk + EU AI Act Assessment + DORA + Relevant ISO/IEC Frameworks + Compliance + Operational Resilience + Continuous Monitoring + Tested Rollback**

This separation demonstrates a realistic path from an **academic prototype to a bank-grade production solution** without claiming that enterprise banking controls have already been implemented.
