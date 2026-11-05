"""
Script to generate the complete PowerPoint Presentation (.pptx)
for CardioDiab-AI: Chronic Disease Risk Prediction System
Using python-pptx with clean modern slide formatting.
"""

import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # Blank layout

    # Color Palette: Modern Clean Academic Theme
    C_NAVY = RGBColor(26, 54, 93)       # #1a365d
    C_BLUE = RGBColor(37, 99, 235)      # #2563eb
    C_TEXT = RGBColor(30, 41, 59)       # #1e293b
    C_MUTED = RGBColor(100, 116, 139)   # #64748b
    C_BG = RGBColor(248, 250, 252)      # #f8fafc
    C_WHITE = RGBColor(255, 255, 255)
    C_CARD_BG = RGBColor(241, 245, 249) # #f1f5f9
    C_GREEN = RGBColor(16, 185, 129)
    C_AMBER = RGBColor(245, 158, 11)

    def add_header(slide, title_text, category="CardioDiab-AI | IBM watsonx.ai Project Presentation"):
        # Top accent bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.1))
        bar.fill.solid()
        bar.fill.fore_color.rgb = C_BLUE
        bar.line.fill.background()

        # Category / breadcrumb
        tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        p_cat = tb_cat.text_frame.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = C_BLUE
        p_cat.font.name = "Arial"

        # Main Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        p_title = tb_title.text_frame.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = C_NAVY
        p_title.font.name = "Arial"

    # ==================== SLIDE 1: TITLE SLIDE ====================
    slide1 = prs.slides.add_slide(blank_layout)
    # Background card
    bg = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_BG
    bg.line.fill.background()

    # Top accent line
    bar1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.15))
    bar1.fill.solid()
    bar1.fill.fore_color.rgb = C_BLUE
    bar1.line.fill.background()

    # Main Card
    card1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.0), Inches(10.9), Inches(5.5))
    card1.fill.solid()
    card1.fill.fore_color.rgb = C_WHITE
    card1.line.color.rgb = RGBColor(226, 232, 240)

    # Title box
    tb = slide1.shapes.add_textbox(Inches(1.8), Inches(1.5), Inches(9.7), Inches(2.5))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "CardioDiab-AI"
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = C_NAVY
    p.font.name = "Arial"

    p2 = tf.add_paragraph()
    p2.text = "Chronic Disease Risk Prediction Model using IBM watsonx.ai Studio"
    p2.font.size = Pt(20)
    p2.font.color.rgb = C_BLUE
    p2.font.name = "Arial"
    p2.space_before = Pt(8)

    p3 = tf.add_paragraph()
    p3.text = "Dual-Disease Clinical Risk Stratification for Type-2 Diabetes & Coronary Heart Disease"
    p3.font.size = Pt(14)
    p3.font.color.rgb = C_MUTED
    p3.font.name = "Arial"
    p3.space_before = Pt(6)

    # Details box
    tb_meta = slide1.shapes.add_textbox(Inches(1.8), Inches(4.3), Inches(9.7), Inches(1.8))
    tf_m = tb_meta.text_frame
    
    pm1 = tf_m.paragraphs[0]
    pm1.text = "• Subject: IBM Applied Artificial Intelligence / Machine Learning with Watson"
    pm1.font.size = Pt(13)
    pm1.font.color.rgb = C_TEXT
    pm1.font.bold = True

    pm2 = tf_m.add_paragraph()
    pm2.text = "• Academic Level: Second Year Engineering College Project & Demo Presentation"
    pm2.font.size = Pt(13)
    pm2.font.color.rgb = C_TEXT
    pm2.space_before = Pt(4)

    pm3 = tf_m.add_paragraph()
    pm3.text = "• Technology Stack: Python, Scikit-Learn, Flask, IBM watsonx AutoAI, HTML5/CSS3"
    pm3.font.size = Pt(13)
    pm3.font.color.rgb = C_MUTED
    pm3.space_before = Pt(4)

    # ==================== SLIDE 2: PROBLEM STATEMENT ====================
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "1. Problem Statement & Motivation")

    def create_card(slide, left, top, width, height, title, items, badge=""):
        c = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        c.fill.solid()
        c.fill.fore_color.rgb = C_WHITE
        c.line.color.rgb = RGBColor(226, 232, 240)

        tb = slide.shapes.add_textbox(Inches(left + 0.3), Inches(top + 0.3), Inches(width - 0.6), Inches(height - 0.6))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = C_NAVY
        p.font.name = "Arial"

        for it in items:
            p_it = tf.add_paragraph()
            p_it.text = f"•  {it}"
            p_it.font.size = Pt(13)
            p_it.font.color.rgb = C_TEXT
            p_it.space_before = Pt(10)
            p_it.font.name = "Arial"

    create_card(slide2, 0.8, 1.8, 5.6, 5.0, "Clinical Challenge", [
        "Cardiovascular diseases and Diabetes are the leading causes of global mortality (>18M deaths annually).",
        "Both conditions often develop asymptomatically in early stages ('Silent Killers').",
        "Traditional diagnostic workflows are slow, resource-intensive, and inaccessible in rural communities.",
        "Clinical consultations often occur after irreversible microvascular damage has already developed."
    ])

    create_card(slide2, 6.9, 1.8, 5.6, 5.0, "The Proposed AI Solution", [
        "Early non-invasive screening using readily accessible biometric indicators (blood sugar, BMI, BP, ECG).",
        "Automated risk scoring using enterprise IBM watsonx.ai Studio / AutoAI methodology.",
        "Simultaneous multi-disease detection: Covers both Type-2 Diabetes and Coronary Heart Disease.",
        "Provides Explainable AI: Highlights primary risk drivers (e.g. Glucose > 140 mg/dL, Exercise Angina) to guide clinicians."
    ])

    # ==================== SLIDE 3: PROJECT OBJECTIVES ====================
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "2. Project Objectives & Core Scope")

    create_card(slide3, 0.8, 1.8, 3.6, 5.0, "1. Predictive Modeling", [
        "Train high-accuracy classification pipelines for Diabetes (Pima benchmark) & Heart Disease (UCI Cleveland).",
        "Benchmark multiple ML algorithms (Random Forest, Extra Trees, Gradient Boosting, Logistic Regression).",
        "Target >85% accuracy and >90% ROC-AUC on heart risk identification."
    ])

    create_card(slide3, 4.8, 1.8, 3.6, 5.0, "2. IBM watsonx.ai Integration", [
        "Follow IBM Watson AutoAI lifecycle: Data cleansing, zero imputation, HPO, and pipeline ranking.",
        "Dual-Engine Architecture: Support both local pre-trained AutoAI exports and live IBM Cloud WML REST scoring.",
        "Provide 100% offline operational reliability for academic presentation and lab demonstration."
    ])

    create_card(slide3, 8.8, 1.8, 3.6, 5.0, "3. Clinical Decision Support", [
        "Build a clean, light, zero-dependency web interface (No NPM, pure Python + standard web stack).",
        "Provide 1-click preset profiles (Healthy, Medium, High Risk) for instant oral presentation.",
        "Generate evidence-based medical recommendations and printable patient summary reports."
    ])

    # ==================== SLIDE 4: SYSTEM ARCHITECTURE ====================
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "3. System Architecture & Workflow")

    create_card(slide4, 0.8, 1.8, 11.7, 5.0, "High-Level Architecture Pipeline", [
        "LAYER 1: CLINICIAN / USER DASHBOARD (HTML5, CSS3, Vanilla JS)",
        "   - Clean medical input form with physiological boundary validation.",
        "   - 1-Click presentation presets (Low Risk, Medium Risk, High Risk) for rapid demonstration.",
        "LAYER 2: BACKEND APPLICATION SERVER (Python Flask 3.1 REST API)",
        "   - Routes: /api/predict/diabetes, /api/predict/heart, /api/metrics, /api/presets.",
        "   - Safe biological zero fallback (auto-imputes impossible zeros to population medians).",
        "LAYER 3: DUAL-ENGINE INFERENCE HUB",
        "   - Engine Mode A (Local): Champion Random Forest Pipeline (.joblib) with StandardScaler (0ms latency, offline).",
        "   - Engine Mode B (Cloud): IBM Cloud IAM OAuth 2.0 Token Exchange -> Watson Machine Learning REST Scoring Endpoint.",
        "LAYER 4: CLINICAL INTERPRETABILITY ENGINE",
        "   - Computes calibrated risk probability (0% - 100%) and categorizes severity (Low / Moderate / High).",
        "   - Highlights primary contributing biomarkers and generates actionable preventive recommendations."
    ])

    # ==================== SLIDE 5: DATASETS & PREPROCESSING ====================
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "4. Benchmark Datasets & Preprocessing")

    create_card(slide5, 0.8, 1.8, 5.6, 5.0, "Pima Indians Diabetes Dataset", [
        "Dataset Source: National Institute of Diabetes and Digestive and Kidney Diseases (768 records).",
        "Target: Binary classification (0 = Non-Diabetic, 1 = Diabetic Positive).",
        "8 Biomarkers: Pregnancies, Glucose, Blood Pressure, Skin Thickness, Insulin, BMI, Pedigree Function (DPF), Age.",
        "Biological Zero Imputation: Zero values in Glucose, Blood Pressure, and BMI represent missing lab records. AutoAI cleans this by imputing positive medians.",
        "StandardScaler applied to normalize metabolic variance."
    ])

    create_card(slide5, 6.9, 1.8, 5.6, 5.0, "UCI Cleveland Heart Disease Dataset", [
        "Dataset Source: University of California Irvine (UCI) Machine Learning Repository (303 patient records).",
        "Target: Binary diagnosis (0 = Healthy Coronary Circulation, 1 = Coronary Artery Disease).",
        "13 Clinical Features: Age, Sex, Chest Pain (cp), Resting BP (trestbps), Cholesterol (chol), Fasting Sugar (fbs), ECG (restecg), Max Heart Rate (thalach), Exercise Angina (exang), ST Depression (oldpeak), Slope, Blocked Vessels (ca), Thalassemia (thal).",
        "Feature Transformation: Standard scaling applied to align continuous hemodynamic and stress test metrics."
    ])

    # ==================== SLIDE 6: IBM WATSONX AUTOAI WORKFLOW ====================
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "5. IBM watsonx.ai Studio & AutoAI Workflow")

    create_card(slide6, 0.8, 1.8, 11.7, 5.0, "5-Stage IBM Watson AutoAI Methodology", [
        "Stage 1: Data Ingestion & Asset Registration",
        "   - Clinical datasets uploaded to IBM Cloud Object Storage (COS) and registered as Watson Data Assets.",
        "Stage 2: Automated Data Cleansing & Preprocessing",
        "   - AutoAI performs automated data profiling, type detection, and biological missing value replacement.",
        "Stage 3: Automated Model Selection & Hyperparameter Optimization (HPO)",
        "   - Evaluates 4 candidate pipelines: Logistic Regression, Random Forest, Extra Trees, and Gradient Boosting.",
        "   - Executes Bayesian Hyperparameter Optimization (tuning n_estimators, max_depth, min_samples_split).",
        "Stage 4: Leaderboard Generation & Champion Selection",
        "   - Ranks pipelines using Stratified K-Fold Cross-Validation, optimizing for ROC-AUC and Recall.",
        "Stage 5: Deployment to Watson Machine Learning (WML)",
        "   - Champion model promoted to an IBM Cloud Deployment Space and exposed via real-time online REST scoring URL."
    ])

    # ==================== SLIDE 7: MACHINE LEARNING ALGORITHMS ====================
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "6. Machine Learning Algorithms & Selection")

    create_card(slide7, 0.8, 1.8, 5.6, 5.0, "Why Random Forest & Ensemble Trees?", [
        "Ensemble Methodology: Combines hundreds of de-correlated decision trees trained on bootstrap samples (Bagging).",
        "Non-Linear Interactions: Perfectly models complex physiological interactions (e.g., high Glucose combined with elevated BMI and Age).",
        "Robust Against Overfitting: Subsampling features at each tree split reduces variance and prevents memorizing training noise.",
        "Intrinsic Feature Importance: Calculates Gini impurity reduction to identify which biomarkers contribute most to risk."
    ])

    create_card(slide7, 6.9, 1.8, 5.6, 5.0, "Champion Pipelines Selected", [
        "Diabetes Champion: AutoAI Pipeline P2 (Random Forest + HPO)",
        "   - Parameters: n_estimators=150, max_depth=6, min_samples_split=4, StandardScaler.",
        "   - Result: 75.32% Accuracy, 80.93% ROC-AUC on holdout test data.",
        "Heart Disease Champion: AutoAI Pipeline P2 (Random Forest + HPO)",
        "   - Parameters: n_estimators=120, max_depth=5, min_samples_split=4, StandardScaler.",
        "   - Result: 88.52% Accuracy, 95.02% ROC-AUC on holdout test data.",
        "Cross-Validated: 80/20 stratified split ensures balanced class distribution across training and testing."
    ])

    # ==================== SLIDE 8: MODEL PERFORMANCE METRICS ====================
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "7. Model Performance & Evaluation Metrics")

    # Table for metrics
    rows, cols = 5, 4
    left, top, width, height = Inches(0.8), Inches(1.8), Inches(11.7), Inches(2.2)
    tbl_shape = slide8.shapes.add_table(rows, cols, left, top, width, height)
    tbl = tbl_shape.table

    headers = ["Evaluation Metric", "Heart Disease Model (Champion)", "Diabetes Model (Champion)", "Clinical Significance"]
    data = [
        ["Accuracy", "88.52%", "75.32%", "Overall proportion of correct classifications"],
        ["ROC - AUC", "95.02%", "80.93%", "Model ability to distinguish disease vs healthy across all thresholds"],
        ["Precision", "83.87%", "66.67%", "Proportion of positive alerts that were genuinely positive"],
        ["Recall (Sensitivity)", "92.86%", "64.58%", "Critical Metric: Minimizes dangerous False Negatives (missed sick patients)"]
    ]

    for col_idx, h in enumerate(headers):
        cell = tbl.cell(0, col_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_NAVY
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.color.rgb = C_WHITE
            p.font.size = Pt(13)

    for row_idx, row_data in enumerate(data):
        for col_idx, val in enumerate(row_data):
            cell = tbl.cell(row_idx + 1, col_idx)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = C_WHITE if row_idx % 2 == 0 else C_CARD_BG
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(12)
                p.font.color.rgb = C_TEXT
                if col_idx in [1, 2]:
                    p.font.bold = True
                    p.font.color.rgb = C_BLUE

    create_card(slide8, 0.8, 4.3, 11.7, 2.5, "Confusion Matrix Analysis (Holdout Test Split)", [
        "Heart Disease Matrix: True Negatives (TN) = 28 | False Positives (FP) = 5 | False Negatives (FN) = 2 | True Positives (TP) = 26",
        "Remarkable Clinical Result: Out of 28 cardiac risk patients, 26 were correctly detected (92.86% Recall). Only 2 cases missed.",
        "Diabetes Matrix: True Negatives (TN) = 85 | False Positives (FP) = 15 | False Negatives (FN) = 17 | True Positives (TP) = 31",
        "Clinical Priority: High Recall is prioritized over Precision in medical screening to ensure patients receive timely confirmatory laboratory testing."
    ])

    # ==================== SLIDE 9: FEATURE IMPORTANCE ====================
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "8. Top Contributing Biomarkers (Feature Importance)")

    create_card(slide9, 0.8, 1.8, 5.6, 5.0, "Diabetes Model (AutoAI Weights)", [
        "1. Fasting Glucose (34.23%): Primary risk indicator. Glucose > 140 mg/dL strongly shifts probability into the Diabetic category.",
        "2. Body Mass Index - BMI (17.44%): Indicates metabolic load and adipose tissue insulin resistance.",
        "3. Patient Age (11.37%): Risk accelerates significantly above 45 years of age.",
        "4. Pedigree Function (DPF) (10.15%): Genetic heredity and familial predisposition.",
        "5. Blood Pressure (9.28%): Diastolic hypertension commonly co-occurs with insulin resistance."
    ])

    create_card(slide9, 6.9, 1.8, 5.6, 5.0, "Heart Disease Model (AutoAI Weights)", [
        "1. Thalassemia Defect (17.90%): Microvascular blood circulation anomalies detected during stress scans.",
        "2. Chest Pain Type (14.70%): Typical angina and non-anginal tightness represent major coronary indicators.",
        "3. Major Blocked Vessels (11.57%): Number of vessels visible under fluoroscopy (0 to 3).",
        "4. Maximum Heart Rate (11.54%): Inability to reach demographic target heart rate (220 - Age).",
        "5. Exercise Induced Angina (11.20%): Myocardial oxygen starvation upon physical exertion."
    ])

    # ==================== SLIDE 10: WEB APP & CLINICAL DECISION SUPPORT ====================
    slide10 = prs.slides.add_slide(blank_layout)
    add_header(slide10, "9. Web Application & Clinical Decision Support")

    create_card(slide10, 0.8, 1.8, 5.6, 5.0, "Front-End Architecture", [
        "Built with vanilla HTML5, CSS3, and JavaScript — Zero NPM, zero Node.js build overhead.",
        "Lightweight, clean, modern medical dashboard optimized for laptop and classroom projector display.",
        "1-Click Sample Presets: Enables instant oral presentation by loading Healthy, Medium, or High Risk patients in 1 click.",
        "Visual Risk Dial: Animated circular probability meter displaying exact risk percentages (0% to 100%).",
        "Color-Coded Status: Safe (Green), Moderate (Amber), High Risk (Red)."
    ])

    create_card(slide10, 6.9, 1.8, 5.6, 5.0, "Clinical Decision Support Features", [
        "Transparent Diagnostic Summary: Explains model prediction in clear, accessible language without medical jargon.",
        "Biomarker Flagging: Automatically flags abnormal values (e.g. 'High Sugar: 178 mg/dL', 'Exercise Angina present').",
        "Evidence-Based Lifestyle Guidance: Suggests diet modifications, exercise regimens, and laboratory confirmatory tests (HbA1c, 12-lead ECG).",
        "Export Clinical Summary (PDF): Generates a printable patient diagnostic card directly from the browser.",
        "Dual Engine Toggle: Easy cloud API modal to switch between offline local model and live IBM Cloud watsonx.ai."
    ])

    # ==================== SLIDE 11: VIVA DEFENSE & EXAMINER Q&A ====================
    slide11 = prs.slides.add_slide(blank_layout)
    add_header(slide11, "10. Key Viva Questions & Technical Defense")

    create_card(slide11, 0.8, 1.8, 5.6, 5.0, "Common Examiner Questions (Part 1)", [
        "Q1: Why did you choose Random Forest over Deep Learning?",
        "Ans: On tabular clinical datasets (300-800 rows), Deep Learning tends to overfit. Random Forest ensembles provide superior generalization, built-in feature importance, and require no heavy GPU hardware.",
        "Q2: How are missing biological values handled?",
        "Ans: Zeroes in Glucose, Blood Pressure, or BMI are biologically impossible in living patients. The system automatically imputes the median of valid positive records during preprocessing and inference."
    ])

    create_card(slide11, 6.9, 1.8, 5.6, 5.0, "Common Examiner Questions (Part 2)", [
        "Q3: How does the application connect to IBM Cloud watsonx.ai?",
        "Ans: Via REST API. The app POSTs the IBM Cloud API Key to the IAM endpoint (https://iam.cloud.ibm.com/identity/token) to obtain an OAuth 2.0 Bearer token, then sends the patient feature payload to the WML scoring endpoint.",
        "Q4: How do you prevent overfitting?",
        "Ans: Using 80/20 stratified train-test splits, 5-fold cross-validation during AutoAI optimization, tree depth restrictions (max_depth=5), and StandardScaler feature scaling."
    ])

    # ==================== SLIDE 12: CONCLUSION & FUTURE SCOPE ====================
    slide12 = prs.slides.add_slide(blank_layout)
    add_header(slide12, "11. Conclusion & Future Roadmap")

    create_card(slide12, 0.8, 1.8, 5.6, 5.0, "Project Summary", [
        "Successfully implemented an end-to-end dual chronic disease risk prediction system following IBM watsonx.ai AutoAI methodology.",
        "Achieved high clinical accuracy: 88.52% on Heart Disease (95.02% ROC-AUC) and 75.32% on Diabetes (80.93% ROC-AUC).",
        "Dual-engine flexibility ensures guaranteed offline reliability during college demos alongside cloud REST readiness.",
        "Provides an intuitive, lightweight interface with clear explainability and actionable medical guidance."
    ])

    create_card(slide12, 6.9, 1.8, 5.6, 5.0, "Future Scope", [
        "EHR / FHIR Integration: Connect directly with hospital Electronic Health Records using HL7 / FHIR protocols.",
        "Mobile Application: Develop a Flutter / React Native smartphone companion for at-home patient monitoring.",
        "Watsonx Governance: Implement automated model drift detection and algorithmic fairness monitoring.",
        "Multi-modal AI: Incorporate actual patient ECG waveform image classification using Convolutional Neural Networks (CNN)."
    ])

    out_path = r"d:\StudyMaterial\watsonx_disease_prediction\CardioDiab_AI_Presentation.pptx"
    prs.save(out_path)
    print(f"[OK] Presentation successfully generated: {out_path}")

if __name__ == "__main__":
    create_deck()
