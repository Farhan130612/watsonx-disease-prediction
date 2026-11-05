# CardioDiab-AI: Viva Presentation & Examiner Q&A Guide
### Second Year Engineering Project (IBM Subject / Applied AI Curriculum)

---

## 1. Project Title & Executive Summary
- **Project Title:** CardioDiab-AI: Chronic Disease Risk Prediction System using IBM watsonx.ai Studio & AutoAI Pipelines.
- **Domain:** Healthcare Predictive Analytics & Machine Learning.
- **Target Diseases:** 
  1. Type-2 Diabetes Mellitus
  2. Coronary Heart Disease (Atherosclerosis / Ischemia)
- **Primary Technology Stack:** 
  - **Platform:** IBM watsonx.ai Studio / IBM Watson Machine Learning (WML).
  - **AutoML Engine:** Watson AutoAI Pipeline Generation (Data Imputation, Feature Transformation, Hyperparameter Optimization).
  - **Backend Server:** Python Flask (Clean micro-REST architecture).
  - **Frontend:** Pure HTML5, CSS3, Vanilla JavaScript (Zero npm, zero build dependencies, ultra-lightweight).

---

## 2. High-Level System Architecture

```
+-------------------------------------------------------------+
|                     User / Clinician UI                     |
|           (IBM Carbon Inspired Responsive Dashboard)        |
+-------------------------------------------------------------+
                              |
                     [HTTP REST JSON API]
                              |
                              v
+-------------------------------------------------------------+
|                      Flask Application                      |
|                  (Prediction & Scoring Hub)                 |
+-------------------------------------------------------------+
         |                                           |
         v                                           v
[Engine Mode: LOCAL]                       [Engine Mode: CLOUD]
Local Watson AutoAI Model Export           IBM watsonx.ai Studio
- Pretrained Pipeline (.joblib)            - IAM OAuth 2.0 Token Exchange
- StandardScaler + ExtraTrees/RF           - Watson Machine Learning Endpoint
- Instant 0ms latency offline              - Online Real-time Cloud Scoring
```

---

## 3. Dataset Benchmarks & Features

### A. Diabetes (Pima Indians Benchmark - 768 Records)
- **Pregnancies:** Gestational frequency.
- **Glucose:** 2-hour post-load plasma glucose (mg/dL) — **Top Contributing Biomarker**.
- **BloodPressure:** Diastolic blood pressure (mm Hg).
- **SkinThickness:** Triceps skin fold thickness (mm).
- **Insulin:** 2-Hour serum insulin (μU/mL).
- **BMI:** Body Mass Index ($kg/m^2$) — **Key Metabolic Indicator**.
- **DiabetesPedigreeFunction (DPF):** Genetic predisposition score.
- **Age:** Patient age in years.
- **Target:** Outcome (0 = Negative, 1 = Diabetic Positive).

### B. Heart Disease (UCI Cleveland Benchmark - 303 Records)
- **age:** Age in years.
- **sex:** 1 = Male, 0 = Female.
- **cp:** Chest pain type (0: Typical Angina, 1: Atypical, 2: Non-Anginal, 3: Asymptomatic).
- **trestbps:** Resting blood pressure on hospital admission (mm Hg).
- **chol:** Serum cholesterol (mg/dL).
- **fbs:** Fasting blood sugar > 120 mg/dL (1 = True, 0 = False).
- **restecg:** Resting electrocardiogram readings (0, 1, 2).
- **thalach:** Maximum heart rate achieved during stress test.
- **exang:** Exercise-induced angina (1 = Yes, 0 = No) — **Primary Ischemia Factor**.
- **oldpeak:** ST depression induced by exercise relative to rest (mm).
- **slope:** Slope of peak exercise ST segment.
- **ca:** Number of major fluoroscopy-stained coronary vessels (0–3).
- **thal:** Thalassemia blood flow perfusion (1 = Fixed defect, 2 = Normal, 3 = Reversible defect).
- **Target:** Heart Disease status (0 = Normal, 1 = Heart Disease).

---

## 4. Top 15 External Examiner Viva Questions & Answers

### Q1: What is IBM watsonx.ai Studio and what problem does it solve?
> **Answer:** IBM watsonx.ai Studio is an enterprise studio for AI builders that combines generative AI foundation models and traditional machine learning. It streamlines the lifecycle of models from data ingestion in Cloud Object Storage (COS), automated pipeline experimentation via AutoAI, model deployment via Watson Machine Learning (WML), and governance.

### Q2: How does Watson AutoAI work?
> **Answer:** AutoAI automates five labor-intensive steps:
> 1. Data preprocessing and type inference.
> 2. Automated data cleansing and biological missing value imputation.
> 3. Candidate algorithm selection (Random Forest, Gradient Boosting, Extra Trees, Logistic Regression).
> 4. Hyperparameter Optimization (HPO) using Bayesian optimization.
> 5. Automated Feature Engineering (generating non-linear polynomial and interaction features).

### Q3: Why did you build a Dual-Engine architecture (Local + Cloud)?
> **Answer:** In real-world hospital environments and academic evaluations, internet connectivity or cloud API token expiration can cause catastrophic downtime. The local engine runs an exact exported Watson AutoAI pipeline ensuring 100% offline uptime with zero latency, while the cloud connector demonstrates production REST integration with IBM Cloud watsonx.ai.

### Q4: Why are physiological zeroes treated as missing data in the Diabetes dataset?
> **Answer:** In living human patients, Glucose, Blood Pressure, BMI, and Insulin can never biologically be 0. These zeros represent missing sensor or lab records. Leaving them as 0 would distort distance-based metrics and tree splits. AutoAI cleans this by imputing the median of valid positive records.

### Q5: Why is Recall (Sensitivity) often more important than Accuracy in healthcare?
> **Answer:** In clinical diagnosis, a **False Negative** (diagnosing a sick patient as healthy) can be fatal because treatment is delayed. A False Positive results only in an additional lab test (like an OGTT or angiogram). Therefore, high Recall ($\frac{TP}{TP + FN}$) is prioritized alongside ROC-AUC.

### Q6: What is the significance of the ROC-AUC score?
> **Answer:** ROC-AUC measures the area under the Receiver Operating Characteristic curve (True Positive Rate vs. False Positive Rate across all classification thresholds). An AUC of 0.85+ signifies that the model has an 85% probability of ranking a random positive disease case higher than a random negative case, regardless of threshold.

### Q7: Explain the Random Forest and Extra Trees algorithms used in your pipelines.
> **Answer:** Random Forest is an ensemble of decision trees trained on bootstrap samples (bagging) with random feature subsets at each split. Extra Trees (Extremely Randomized Trees) takes randomization further by testing random cut-points for feature thresholds, which reduces model variance and computational overhead while maintaining high generalization accuracy.

### Q8: What are the top risk drivers identified by the model for Heart Disease?
> **Answer:** Based on feature importance analysis, the top three clinical indicators are:
> 1. `exang` (Exercise Induced Angina): Signifies myocardial oxygen deficit during stress.
> 2. `cp` (Chest pain classification): Specifically typical angina.
> 3. `thal` (Thalassemia defect): Indicates microvascular perfusion anomalies.

### Q9: How does the application authenticate with IBM Cloud in production?
> **Answer:** It uses the OAuth 2.0 standard. The application issues an HTTP POST to `https://iam.cloud.ibm.com/identity/token` passing the IBM Cloud API key, receives a signed Bearer JWT token, and passes this token in the `Authorization: Bearer <token>` header to the Watson Machine Learning scoring endpoint.

### Q10: How do you prevent overfitting?
> **Answer:** Through:
> 1. Stratified 80/20 train-test splits.
> 2. K-Fold cross-validation during AutoAI optimization.
> 3. Limiting maximum tree depth (`max_depth=5-6`) and enforcing minimum leaf samples (`min_samples_leaf=2`).
> 4. Regularization and feature scaling via `StandardScaler`.

### Q11: What is the role of `StandardScaler` in the pipeline?
> **Answer:** Features like Cholesterol (100–500 mg/dL) have vastly different numerical ranges compared to Oldpeak (0.0–6.0 mm). `StandardScaler` standardizes each feature to have a mean of 0 and a standard deviation of 1 ($z = \frac{x - \mu}{\sigma}$), preventing dominant numerical scales from biasing distance metrics and gradient updates.

### Q12: Why did you not use heavy frameworks like React, Node.js, or NPM?
> **Answer:** To keep the project robust, lightweight, and universally runnable on any student or examiner laptop without dependency collisions, node_modules bloat, or complex compilation steps. Vanilla web standards (HTML5/CSS3/ES6) ensure instant loading, zero maintenance overhead, and maximum reliability.

### Q13: Can you explain the Confusion Matrix metrics in your app?
> **Answer:** 
> - **True Negative (TN):** Healthy patients correctly classified as low risk.
> - **False Positive (FP):** Healthy patients classified as high risk (Type I error).
> - **False Negative (FN):** Diseased patients mistakenly classified as low risk (Type II error).
> - **True Positive (TP):** Diseased patients correctly identified.

### Q14: How does your system assist clinical decision-making?
> **Answer:** It does not replace physicians; it acts as a clinical decision support system (CDSS). It highlights specific abnormal biomarkers (e.g., elevated diastolic pressure, glucose $> 140$ mg/dL) and suggests confirmatory lab tests (HbA1c, 12-lead ECG, stress echocardiography) and evidence-based lifestyle interventions.

### Q15: How can this project be scaled or taken to production?
> **Answer:**
> 1. Containerization using Docker and deployment on IBM Cloud Code Engine or Red Hat OpenShift.
> 2. Integrating electronic health record (EHR) systems using HL7 / FHIR API protocols.
> 3. Adding explainable AI (XAI) using IBM watsonx.governance for model bias and drift monitoring.
