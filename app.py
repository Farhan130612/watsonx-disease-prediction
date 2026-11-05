"""
CardioDiab-AI: Diabetes & Heart Disease Risk Prediction System
Using IBM watsonx.ai Studio / Watson AutoAI Pipeline Architecture
Second Year Engineering Project (IBM Applied AI)
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from watsonx.watsonx_client import WatsonxClient

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
CORS(app)

# Load trained pipelines & metrics
diabetes_model_path = os.path.join(MODELS_DIR, 'diabetes_model.joblib')
heart_model_path = os.path.join(MODELS_DIR, 'heart_model.joblib')
metrics_path = os.path.join(MODELS_DIR, 'metrics.json')

diabetes_pipeline = None
heart_pipeline = None
model_metrics = {}

try:
    if os.path.exists(diabetes_model_path):
        diabetes_pipeline = joblib.load(diabetes_model_path)
    if os.path.exists(heart_model_path):
        heart_pipeline = joblib.load(heart_model_path)
    if os.path.exists(metrics_path):
        with open(metrics_path, 'r', encoding='utf-8') as f:
            model_metrics = json.load(f)
except Exception as e:
    print(f"[!] Warning during model load: {e}")

# Preset Patient Profiles for Instant Demo Presentation
PRESET_PROFILES = {
    "diabetes": {
        "low_risk": {
            "name": "Sample 1 (Healthy - Low Risk)",
            "pregnancies": 1,
            "glucose": 95,
            "blood_pressure": 70,
            "skin_thickness": 20,
            "insulin": 80,
            "bmi": 22.5,
            "dpf": 0.25,
            "age": 24
        },
        "borderline_risk": {
            "name": "Sample 2 (Average - Medium Risk)",
            "pregnancies": 2,
            "glucose": 132,
            "blood_pressure": 82,
            "skin_thickness": 28,
            "insulin": 140,
            "bmi": 28.4,
            "dpf": 0.52,
            "age": 42
        },
        "high_risk": {
            "name": "Sample 3 (At Risk - High Risk)",
            "pregnancies": 6,
            "glucose": 178,
            "blood_pressure": 94,
            "skin_thickness": 38,
            "insulin": 210,
            "bmi": 36.8,
            "dpf": 0.85,
            "age": 54
        }
    },
    "heart": {
        "low_risk": {
            "name": "Sample 1 (Healthy - Low Risk)",
            "age": 38,
            "sex": 0,
            "cp": 1,
            "trestbps": 118,
            "chol": 182,
            "fbs": 0,
            "restecg": 0,
            "thalach": 168,
            "exang": 0,
            "oldpeak": 0.2,
            "slope": 0,
            "ca": 0,
            "thal": 0
        },
        "borderline_risk": {
            "name": "Sample 2 (Average - Medium Risk)",
            "age": 52,
            "sex": 1,
            "cp": 2,
            "trestbps": 135,
            "chol": 238,
            "fbs": 0,
            "restecg": 1,
            "thalach": 140,
            "exang": 0,
            "oldpeak": 1.4,
            "slope": 1,
            "ca": 1,
            "thal": 0
        },
        "high_risk": {
            "name": "Sample 3 (At Risk - High Risk)",
            "age": 63,
            "sex": 1,
            "cp": 3,
            "trestbps": 165,
            "chol": 295,
            "fbs": 1,
            "restecg": 2,
            "thalach": 115,
            "exang": 1,
            "oldpeak": 2.8,
            "slope": 1,
            "ca": 2,
            "thal": 2
        }
    }
}

@app.route('/')
def home():
    """Render main web application interface."""
    return render_template('index.html')

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    """Return model evaluation metrics, leaderboard and feature rankings."""
    return jsonify({
        "status": "success",
        "data": model_metrics
    })

@app.route('/api/presets', methods=['GET'])
def get_presets():
    """Return presentation test profiles for quick 1-click loading."""
    return jsonify({
        "status": "success",
        "data": PRESET_PROFILES
    })

@app.route('/api/predict/diabetes', methods=['POST'])
def predict_diabetes():
    """
    Run Diabetes Risk Prediction inference.
    Supports Dual-Engine: Local Watson AutoAI Pipeline OR Cloud watsonx.ai scoring.
    """
    try:
        req = request.get_json(force=True)
        engine = req.get('engine', 'local')
        
        # Extract features with safe medical defaults
        pregnancies = float(req.get('pregnancies', 0))
        glucose = float(req.get('glucose', 115))
        blood_pressure = float(req.get('blood_pressure', 72))
        skin_thickness = float(req.get('skin_thickness', 23))
        insulin = float(req.get('insulin', 95))
        bmi = float(req.get('bmi', 26.0))
        dpf = float(req.get('dpf', 0.42))
        age = float(req.get('age', 35))
        
        # Clinical zero fallback (living persons cannot have 0 glucose or 0 blood pressure)
        if glucose <= 0: glucose = 117.0
        if blood_pressure <= 0: blood_pressure = 72.0
        if bmi <= 0: bmi = 26.5
        if skin_thickness <= 0: skin_thickness = 23.0
        if insulin <= 0: insulin = 95.0
        if age <= 0: age = 30.0
        
        feature_names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                         'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
        feature_values = [[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]]
        df_input = pd.DataFrame(feature_values, columns=feature_names)
        
        risk_score = 0.0
        prediction = 0
        used_engine = "Local Watson AutoAI Model (Offline)"
        
        # Check if user opted for cloud watsonx.ai
        if engine == 'watsonx' and req.get('ibm_api_key') and req.get('wml_deployment_id'):
            client = WatsonxClient(
                api_key=req.get('ibm_api_key'),
                deployment_id=req.get('wml_deployment_id'),
                service_url=req.get('wml_service_url')
            )
            wml_res = client.predict(feature_names, feature_values)
            prediction = int(wml_res.get('prediction', 0))
            probs = wml_res.get('probability', [0.5, 0.5])
            risk_score = round(probs[1] * 100, 1)
            used_engine = "IBM Cloud watsonx.ai REST API"
        else:
            if diabetes_pipeline is None:
                return jsonify({"status": "error", "message": "Diabetes model not loaded."}), 500
            
            probs = diabetes_pipeline.predict_proba(df_input)[0]
            prediction = int(diabetes_pipeline.predict(df_input)[0])
            risk_score = round(float(probs[1]) * 100, 1)
            used_engine = "Watson AutoAI Random Forest Model (Local)"
            
        # Determine risk category (simple, natural wording)
        if risk_score < 25.0:
            risk_level = "Low Risk"
            risk_color = "success"
            summary = "Safe and healthy. Blood sugar and body weight readings are in a normal range."
        elif risk_score < 55.0:
            risk_level = "Moderate Risk"
            risk_color = "warning"
            summary = "Moderate risk. Blood sugar or BMI is slightly elevated. Simple lifestyle changes can help maintain health."
        else:
            risk_level = "High Risk"
            risk_color = "danger"
            summary = "High risk detected. Blood sugar levels are higher than usual, which indicates a strong risk of diabetes."
            
        # Contributing Factor Analysis (plain, clear language)
        risk_factors = []
        if glucose >= 140:
            risk_factors.append(f"High Blood Sugar (Glucose: {int(glucose)} mg/dL - normal is under 100)")
        elif glucose >= 105:
            risk_factors.append(f"Borderline Blood Sugar (Glucose: {int(glucose)} mg/dL)")
            
        if bmi >= 30:
            risk_factors.append(f"High BMI ({bmi:.1f} kg/m2 - indicates higher body weight)")
        elif bmi >= 25:
            risk_factors.append(f"Slightly Elevated BMI ({bmi:.1f} kg/m2)")
            
        if blood_pressure >= 90:
            risk_factors.append(f"High Blood Pressure ({int(blood_pressure)} mm Hg)")
            
        if age >= 45:
            risk_factors.append(f"Age factor ({int(age)} years old)")
            
        if dpf >= 0.6:
            risk_factors.append("Family history / genetic tendency")
            
        if not risk_factors:
            risk_factors.append("All health numbers are within normal, healthy ranges.")
            
        # Actionable recommendations
        recommendations = [
            "Drink plenty of water and reduce sugary snacks and soda drinks.",
            "Aim for 30 minutes of walking, jogging, or cycling most days.",
            "Add more green vegetables, whole grains, and protein to daily meals.",
            "Get a routine fasting blood sugar test once a year."
        ]
        
        return jsonify({
            "status": "success",
            "prediction": prediction,
            "prediction_label": "Diabetic Risk Positive" if prediction == 1 else "Non-Diabetic",
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_color": risk_color,
            "summary": summary,
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "engine_used": used_engine
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/predict/heart', methods=['POST'])
def predict_heart():
    """
    Run Heart Disease Risk Prediction inference.
    Supports Dual-Engine: Local Watson AutoAI Pipeline OR Cloud watsonx.ai scoring.
    """
    try:
        req = request.get_json(force=True)
        engine = req.get('engine', 'local')
        
        age = float(req.get('age', 45))
        sex = float(req.get('sex', 1))
        cp = float(req.get('cp', 1))
        trestbps = float(req.get('trestbps', 120))
        chol = float(req.get('chol', 210))
        fbs = float(req.get('fbs', 0))
        restecg = float(req.get('restecg', 0))
        thalach = float(req.get('thalach', 150))
        exang = float(req.get('exang', 0))
        oldpeak = float(req.get('oldpeak', 0.5))
        slope = float(req.get('slope', 1))
        ca = float(req.get('ca', 0))
        thal = float(req.get('thal', 0))
        
        # Clinical zero fallback for heart features
        if age <= 0: age = 45.0
        if trestbps <= 0: trestbps = 120.0
        if chol <= 0: chol = 200.0
        if thalach <= 0: thalach = 150.0
        
        feature_names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
                         'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        feature_values = [[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]]
        df_input = pd.DataFrame(feature_values, columns=feature_names)
        
        risk_score = 0.0
        prediction = 0
        used_engine = "Local Watson AutoAI Model (Offline)"
        
        if engine == 'watsonx' and req.get('ibm_api_key') and req.get('wml_deployment_id'):
            client = WatsonxClient(
                api_key=req.get('ibm_api_key'),
                deployment_id=req.get('wml_deployment_id'),
                service_url=req.get('wml_service_url')
            )
            wml_res = client.predict(feature_names, feature_values)
            prediction = int(wml_res.get('prediction', 0))
            probs = wml_res.get('probability', [0.5, 0.5])
            risk_score = round(probs[1] * 100, 1)
            used_engine = "IBM Cloud watsonx.ai REST API"
        else:
            if heart_pipeline is None:
                return jsonify({"status": "error", "message": "Heart disease model not loaded."}), 500
            
            probs = heart_pipeline.predict_proba(df_input)[0]
            prediction = int(heart_pipeline.predict(df_input)[0])
            risk_score = round(float(probs[1]) * 100, 1)
            used_engine = "Watson AutoAI Random Forest Model (Local)"
            
        if risk_score < 30.0:
            risk_level = "Low Risk"
            risk_color = "success"
            summary = "Healthy heart profile. Blood pressure, cholesterol, and heart test readings look good."
        elif risk_score < 60.0:
            risk_level = "Moderate Risk"
            risk_color = "warning"
            summary = "Moderate risk. A few signs like blood pressure or cholesterol are slightly elevated."
        else:
            risk_level = "High Risk"
            risk_color = "danger"
            summary = "High risk detected. Signs like chest pain, exercise stress, or blood pressure indicate potential heart risk."
            
        # Clinical Risk Factors Detection (simplified)
        risk_factors = []
        if exang == 1:
            risk_factors.append("Chest discomfort or tightness occurs during physical activity")
        if oldpeak >= 1.5:
            risk_factors.append(f"High heart stress level during exercise ({oldpeak} mm ST depression)")
        if trestbps >= 140:
            risk_factors.append(f"High Blood Pressure ({int(trestbps)} mm Hg)")
        if chol >= 240:
            risk_factors.append(f"High Cholesterol ({int(chol)} mg/dL - normal is under 200)")
        if ca >= 1:
            risk_factors.append(f"Blocked blood vessels observed ({int(ca)} major vessel(s))")
        if thal > 0:
            risk_factors.append("Irregular blood flow detected in heart scan")
        if thalach < 125:
            risk_factors.append(f"Lower max heart rate achieved ({int(thalach)} bpm)")
            
        if not risk_factors:
            risk_factors.append("Heart rate, blood pressure, and cholesterol are all in a safe range.")
            
        recommendations = [
            "Include 30 minutes of light cardio like brisk walking or cycling daily.",
            "Eat a balanced diet with less fried food, less salt, and more fresh vegetables.",
            "Avoid smoking and manage everyday stress with proper 7-8 hours of sleep.",
            "Check blood pressure and cholesterol levels every 6 to 12 months."
        ]
        
        return jsonify({
            "status": "success",
            "prediction": prediction,
            "prediction_label": "Heart Disease Positive" if prediction == 1 else "Normal Cardiac Function",
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_color": risk_color,
            "summary": summary,
            "risk_factors": risk_factors,
            "recommendations": recommendations,
            "engine_used": used_engine
        })
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    print("=" * 65)
    print(" CardioDiab-AI : IBM watsonx.ai Studio Disease Prediction System")
    print(" Second Year Engineering College Project (IBM Subject)")
    print("=" * 65)
    print(" [OK] Web Server running at: http://127.0.0.1:5000")
    print(" [OK] Dual Disease Prediction: Diabetes & Heart Disease")
    print(" [OK] Engine: Watson AutoAI ML Pipeline Export + Cloud Scoring Connector")
    print("=" * 65)
    app.run(host='127.0.0.1', port=5000, debug=True)
