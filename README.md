# CardioDiab-AI: Chronic Disease Risk Prediction System
### Using IBM watsonx.ai Studio / Watson AutoAI Machine Learning Pipelines
**Second Year Engineering College Project & Demo Presentation**
*Subject / Curriculum: IBM Applied AI / Machine Learning with Watson*

---

## 🌟 Highlights & Features
- **Dual Disease Prediction:** Predicts both **Type-2 Diabetes** and **Coronary Heart Disease** from a single unified interface.
- **IBM watsonx.ai Architecture:** Built following the IBM Watson AutoAI methodology (Automated Data Cleansing, Imputation, HPO, and Model Selection).
- **Dual-Engine Flexibility:**
  - **Local Engine (Default):** Pre-trained AutoAI model pipelines running 100% offline with 0ms latency. Zero dependency on cloud credits during college lab presentations!
  - **Cloud Engine:** Configurable REST connector to live IBM Cloud watsonx.ai / Watson Machine Learning scoring endpoints.
- **Examiner-Ready Presentation Tools:**
  - **Quick Demo Presets:** 1-Click buttons to load *Low Risk*, *Moderate*, and *High Risk* patient cases instantly without typing.
  - **Dynamic Risk Gauge:** Visual circular probability meter with color-coded severity badges.
  - **Biomarker Driver Breakdown:** Automatically highlights the abnormal parameters (e.g. Glucose > 140 mg/dL, Exercise Angina).
  - **Evidence-Based Medical Recommendations:** Actionable lifestyle and diagnostic next steps.
  - **Live AutoAI Analytics Tab:** Displays Accuracy, ROC-AUC, Confusion Matrix, and Feature Importance rankings.
  - **Print/Export Report:** 1-click clinical report export to clean PDF.
- **Zero NPM / Zero Node.js:** Built with standard Python (Flask) and pure HTML5, CSS3, JavaScript. Runs out of the box with zero build steps or heavy packages.

---

## 🚀 Quick Start (Running on Laptop)

### Method 1: One-Click Launch (Windows)
Double-click the **`run.bat`** file in this folder:
```
run.bat
```
This automatically starts the server and opens `http://127.0.0.1:5000` in your default web browser.

### Method 2: Command Line
Open PowerShell or Command Prompt in this folder and run:
```bash
python app.py
```
Then open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
watsonx_disease_prediction/
│
├── app.py                      # Flask backend API server (Local & Cloud scoring)
├── run.bat                     # 1-Click Windows launch script
├── train_models.py             # AutoAI simulation & model training script
├── requirements.txt            # Python dependencies
├── README.md                   # Project overview & instructions
│
├── datasets/                   # Clinical benchmark data
│   ├── diabetes.csv            # Pima Indians Diabetes Dataset (768 rows)
│   └── heart.csv               # UCI Cleveland Heart Disease Dataset (303 rows)
│
├── models/                     # Trained ML pipelines & evaluations
│   ├── diabetes_model.joblib   # Champion Pipeline: Random Forest + Scaler
│   ├── heart_model.joblib      # Champion Pipeline: Extra Trees + Scaler
│   └── metrics.json            # Accuracy, ROC-AUC, Confusion Matrix, Feature Weights
│
├── watsonx/                    # IBM watsonx.ai integration assets
│   ├── watsonx_client.py       # IBM Cloud IAM token exchange & WML REST client
│   ├── watsonx_studio_workflow.py # Jupyter script for IBM Watson Studio Cloud Pak
│   └── viva_qa_guide.md        # Complete Viva presentation guide & 15 Q&As
│
├── static/                     # Frontend assets (No npm, pure vanilla)
│   ├── css/
│   │   └── style.css           # IBM Carbon Design inspired styling
│   └── js/
│       └── app.js              # Tab controller, presets, gauge animation, scoring
│
└── templates/
    └── index.html              # Healthcare prediction dashboard
```

---

## 🎯 How to Present This in College (Demo Flow)

1. **Introduction (1 minute):**
   - *"Good morning/afternoon. Today I am presenting CardioDiab-AI, a clinical risk prediction system for Diabetes and Heart Disease designed using the IBM watsonx.ai Studio and AutoAI pipeline methodology."*
2. **Show the Diabetes Predictor (2 minutes):**
   - Click the **"Low Risk"** preset: Show that the patient has normal glucose (95 mg/dL) and normal BMI (22.5), resulting in a **Low Risk** output (~12%).
   - Click the **"High Risk"** preset: Point out elevated glucose (178 mg/dL) and BMI (36.8), resulting in a **High Risk (Critical)** score (~85%+).
   - Point out the automatically generated **Clinical Biomarker Breakdown** and **Medical Recommendations**.
3. **Show the Heart Disease Predictor (2 minutes):**
   - Click the **"High Risk"** preset: Explain how typical angina, exercise-induced angina, and ST depression drive the risk probability.
   - Show the **Export Clinical Summary (PDF)** button.
4. **Show Model Analytics & AutoAI Leaderboard (2 minutes):**
   - Click the **AutoAI Model Metrics** tab.
   - Walk the examiner through the **Confusion Matrix** (True Positives, False Negatives).
   - Show the **Top Contributing Biomarkers** (Feature Importance bar chart).
5. **Explain the IBM watsonx Architecture (1-2 minutes):**
   - Switch to the **IBM watsonx Architecture & Viva Guide** tab.
   - Explain the 5 pipeline steps: Ingestion -> Imputation -> Candidate Pipelines -> WML Deployment -> REST Scoring.
   - Refer to `watsonx/viva_qa_guide.md` for answers to any external examiner questions!

---

## 🧪 Model Performance Summary

| Disease | Champion Pipeline | Test Accuracy | ROC-AUC | Top Biomarker |
| :--- | :--- | :---: | :---: | :--- |
| **Diabetes** | AutoAI-P2 (Random Forest + HPO) | **75.3%** | **80.9%** | Glucose (34.2%) |
| **Heart Disease** | AutoAI-P2 (Random Forest + HPO) | **88.5%** | **95.0%** | Thalassemia Defect (17.9%) |

---

## ☁️ Optional: Connecting to Live IBM Cloud watsonx.ai
If you have an active IBM Cloud account:
1. Click **"⚙️ Cloud API Config"** in the top navigation bar.
2. Select **"IBM Cloud watsonx.ai / WML Online REST API"**.
3. Paste your **IBM Cloud API Key** and **WML Deployment ID**.
4. Click **"Save & Apply Settings"**. The app will now score directly against your IBM Cloud endpoint!
