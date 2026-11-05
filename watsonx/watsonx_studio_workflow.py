"""
================================================================================
IBM watsonx.ai Studio & Watson Machine Learning (WML) Workflow Script
================================================================================
This script contains the exact code to be executed inside an IBM Watson Studio
Jupyter Notebook or watsonx.ai project environment.

Workflow Stages:
1. Initialize Watson Machine Learning API Client
2. Connect to IBM Cloud Object Storage (COS) & Dataset Asset
3. Configure and Launch Watson AutoAI Experiment
4. Evaluate Candidate Pipelines (Leaderboard)
5. Promote Champion Pipeline to Deployment Space
6. Deploy as an Online Real-time REST API Endpoint
7. Run Inference Scoring Payload
================================================================================
"""

# Step 1: Install & Import IBM Watson ML SDK (if running inside Watson Studio)
# !pip install ibm-watson-machine-learning --upgrade

from ibm_watson_machine_learning import APIClient
import json

# Step 2: Configure IBM Cloud Credentials
wml_credentials = {
    "url": "https://us-south.ml.cloud.ibm.com",   # Change to your Watson region (e.g., eu-de, jp-tok)
    "apikey": "YOUR_IBM_CLOUD_API_KEY_HERE"       # Obtain from IBM Cloud -> Manage -> Access (IAM) -> API Keys
}

client = APIClient(wml_credentials)
print("IBM WML Client Connected successfully.")

# Step 3: Set Space ID or Project ID
# Create a Deployment Space in IBM Cloud Pak for Data / watsonx.ai and paste the ID here:
SPACE_ID = "YOUR_DEPLOYMENT_SPACE_GUID_HERE"
client.set.default_space(SPACE_ID)
print(f"Active Deployment Space set to: {SPACE_ID}")

# Step 4: AutoAI Experiment Configuration (AutoML for Healthcare Risk)
"""
In watsonx.ai Studio UI:
1. Click '+ New Asset' -> 'AutoAI'
2. Name: 'CardioDiab_Risk_Prediction'
3. Associate Data Asset: 'diabetes.csv' or 'heart.csv'
4. Select Prediction Column: 'Outcome' (or 'target' for Heart Disease)
5. Metric Optimization: 'ROC AUC' / 'Accuracy'
6. Algorithms to test: Random Forest, Gradient Boosted Trees, Extra Trees, Logistic Regression
"""

# Programmatic AutoAI execution with Watson Python SDK:
from ibm_watson_machine_learning.experiment import AutoAI

experiment = AutoAI(wml_credentials, space_id=SPACE_ID)
pipeline_optimizer = experiment.optimizer(
    name="CardioDiab_Risk_AutoAI",
    prediction_type=AutoAI.PredictionType.BINARY,
    prediction_column="Outcome",
    scoring=AutoAI.Metrics.ROC_AUC_SCORE,
    holdout_size=0.2,
    max_number_of_estimators=4
)

# Step 5: Save & Deploy Champion Model
"""
Once the AutoAI leaderboard completes:
- Select Pipeline 2 (Random Forest with HPO) or Pipeline 4 (Gradient Boosted Trees)
- Save Model to Space
"""
def deploy_saved_model(model_id, deployment_name="CardioDiab_Online_Service"):
    deployment_details = client.deployments.create(
        artifact_uid=model_id,
        meta_props={
            client.deployments.ConfigurationMetaNames.NAME: deployment_name,
            client.deployments.ConfigurationMetaNames.ONLINE: {}
        }
    )
    deployment_uid = client.deployments.get_uid(deployment_details)
    scoring_url = client.deployments.get_scoring_href(deployment_details)
    print(f"Model Deployed Successfully! Deployment ID: {deployment_uid}")
    print(f"Scoring URL: {scoring_url}")
    return deployment_uid

# Step 6: Test Online Scoring Payload
def test_scoring(deployment_uid):
    payload = {
        client.deployments.ScoringMetaNames.INPUT_DATA: [{
            "fields": ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"],
            "values": [[6, 148, 72, 35, 0, 33.6, 0.627, 50]]
        }]
    }
    result = client.deployments.score(deployment_uid, payload)
    print("Scoring Result from IBM Cloud watsonx.ai:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    print("To execute against live IBM Cloud, provide your API key and Space ID above.")
