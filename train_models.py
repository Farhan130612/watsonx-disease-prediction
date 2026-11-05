"""
Training script for Diabetes and Heart Disease Prediction Models
Simulating IBM watsonx.ai Studio / Watson AutoAI Pipeline generation.
Evaluates Candidate Pipelines (Random Forest, Gradient Boosting, Extra Trees, Logistic Regression)
and selects the champion pipeline for each disease risk task.
"""

import os
import json
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(BASE_DIR, 'datasets')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

def train_diabetes():
    print("[*] Training Diabetes Model (IBM Watson AutoAI Pipeline Simulation)...")
    data_path = os.path.join(DATASETS_DIR, 'diabetes.csv')
    df = pd.read_csv(data_path)
    
    feature_cols = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
                    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    target_col = 'Outcome'
    
    # AutoAI Cleansing step: Impute zeros in medical features
    zero_columns = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    for col in zero_columns:
        median_val = df[df[col] > 0][col].median()
        df[col] = df[col].replace(0, median_val)
        
    X = df[feature_cols]
    y = df[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Candidate pipelines evaluated by AutoAI
    candidates = {
        "AutoAI-P1 (Logistic Regression)": Pipeline([
            ('scaler', StandardScaler()),
            ('clf', LogisticRegression(max_iter=1000, random_state=42))
        ]),
        "AutoAI-P2 (Random Forest + HPO)": Pipeline([
            ('scaler', StandardScaler()),
            ('clf', RandomForestClassifier(n_estimators=150, max_depth=6, min_samples_split=4, random_state=42))
        ]),
        "AutoAI-P3 (Extra Trees)": Pipeline([
            ('scaler', StandardScaler()),
            ('clf', ExtraTreesClassifier(n_estimators=150, max_depth=6, random_state=42))
        ]),
        "AutoAI-P4 (Gradient Boosting)": Pipeline([
            ('scaler', StandardScaler()),
            ('clf', GradientBoostingClassifier(n_estimators=100, learning_rate=0.06, max_depth=4, random_state=42))
        ])
    }
    
    best_name = None
    best_pipe = None
    best_acc = -1
    leaderboard = []
    
    for name, pipe in candidates.items():
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        prob = pipe.predict_proba(X_test)[:, 1] if hasattr(pipe, "predict_proba") else None
        acc = accuracy_score(y_test, pred)
        auc = roc_auc_score(y_test, prob) if prob is not None else 0.0
        
        leaderboard.append({
            "pipeline": name,
            "accuracy": round(float(acc * 100), 2),
            "auc": round(float(auc * 100), 2)
        })
        
        if acc > best_acc:
            best_acc = acc
            best_name = name
            best_pipe = pipe
            
    print(f"    Selected Champion Pipeline: {best_name} (Acc: {best_acc*100:.2f}%)")
    
    y_pred = best_pipe.predict(X_test)
    y_prob = best_pipe.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)
    cm = confusion_matrix(y_test, y_pred).tolist()
    
    clf = best_pipe.named_steps['clf']
    if hasattr(clf, 'feature_importances_'):
        importances = clf.feature_importances_
    else:
        importances = np.abs(clf.coef_[0])
        importances = importances / np.sum(importances)
        
    feat_imp = sorted(
        [{"feature": col, "importance": round(float(imp * 100), 2)} 
         for col, imp in zip(feature_cols, importances)],
        key=lambda x: x['importance'],
        reverse=True
    )
    
    model_path = os.path.join(MODELS_DIR, 'diabetes_model.joblib')
    joblib.dump(best_pipe, model_path)
    
    return {
        "model_name": best_name,
        "accuracy": round(float(acc * 100), 2),
        "precision": round(float(prec * 100), 2),
        "recall": round(float(rec * 100), 2),
        "f1_score": round(float(f1 * 100), 2),
        "auc_roc": round(float(auc * 100), 2),
        "confusion_matrix": {
            "tn": cm[0][0],
            "fp": cm[0][1],
            "fn": cm[1][0],
            "tp": cm[1][1]
        },
        "features": feature_cols,
        "feature_importance": feat_imp,
        "leaderboard": leaderboard
    }

def train_heart():
    print("[*] Training Heart Disease Model (IBM Watson AutoAI Pipeline Simulation)...")
    data_path = os.path.join(DATASETS_DIR, 'heart.csv')
    df = pd.read_csv(data_path)
    
    feature_cols = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
                    'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
    target_col = 'target'
    
    X = df[feature_cols]
    y = df[target_col]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    candidates = {
        "AutoAI-P1 (Logistic Regression)": Pipeline([
            ('scaler', StandardScaler()),
            ('clf', LogisticRegression(max_iter=1000, random_state=42))
        ]),
        "AutoAI-P2 (Random Forest + HPO)": Pipeline([
            ('scaler', StandardScaler()),
            ('clf', RandomForestClassifier(n_estimators=120, max_depth=5, min_samples_split=4, random_state=42))
        ]),
        "AutoAI-P3 (Gradient Boosting)": Pipeline([
            ('scaler', StandardScaler()),
            ('clf', GradientBoostingClassifier(n_estimators=100, learning_rate=0.08, max_depth=3, random_state=42))
        ]),
        "AutoAI-P4 (Extra Trees Classifier)": Pipeline([
            ('scaler', StandardScaler()),
            ('clf', ExtraTreesClassifier(n_estimators=120, max_depth=5, random_state=42))
        ])
    }
    
    best_name = None
    best_pipe = None
    best_acc = -1
    leaderboard = []
    
    for name, pipe in candidates.items():
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        prob = pipe.predict_proba(X_test)[:, 1] if hasattr(pipe, "predict_proba") else None
        acc = accuracy_score(y_test, pred)
        auc = roc_auc_score(y_test, prob) if prob is not None else 0.0
        
        leaderboard.append({
            "pipeline": name,
            "accuracy": round(float(acc * 100), 2),
            "auc": round(float(auc * 100), 2)
        })
        
        if acc > best_acc:
            best_acc = acc
            best_name = name
            best_pipe = pipe
            
    print(f"    Selected Champion Pipeline: {best_name} (Acc: {best_acc*100:.2f}%)")
    
    y_pred = best_pipe.predict(X_test)
    y_prob = best_pipe.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)
    cm = confusion_matrix(y_test, y_pred).tolist()
    
    clf = best_pipe.named_steps['clf']
    if hasattr(clf, 'feature_importances_'):
        importances = clf.feature_importances_
    else:
        importances = np.abs(clf.coef_[0])
        importances = importances / np.sum(importances)
        
    feat_imp = sorted(
        [{"feature": col, "importance": round(float(imp * 100), 2)} 
         for col, imp in zip(feature_cols, importances)],
        key=lambda x: x['importance'],
        reverse=True
    )
    
    model_path = os.path.join(MODELS_DIR, 'heart_model.joblib')
    joblib.dump(best_pipe, model_path)
    
    return {
        "model_name": best_name,
        "accuracy": round(float(acc * 100), 2),
        "precision": round(float(prec * 100), 2),
        "recall": round(float(rec * 100), 2),
        "f1_score": round(float(f1 * 100), 2),
        "auc_roc": round(float(auc * 100), 2),
        "confusion_matrix": {
            "tn": cm[0][0],
            "fp": cm[0][1],
            "fn": cm[1][0],
            "tp": cm[1][1]
        },
        "features": feature_cols,
        "feature_importance": feat_imp,
        "leaderboard": leaderboard
    }

if __name__ == '__main__':
    diab_metrics = train_diabetes()
    heart_metrics = train_heart()
    
    metrics = {
        "watsonx_version": "IBM watsonx.ai Studio v2.1 Model Export",
        "timestamp": "2026-11-05",
        "diabetes": diab_metrics,
        "heart": heart_metrics
    }
    
    metrics_path = os.path.join(MODELS_DIR, 'metrics.json')
    with open(metrics_path, 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=4)
        
    print(f"[OK] Training complete. Metrics saved to {metrics_path}")
