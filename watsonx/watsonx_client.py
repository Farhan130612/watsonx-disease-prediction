"""
IBM watsonx.ai / Watson Machine Learning (WML) Client Module
Handles IAM token generation and online scoring against IBM Cloud endpoints.
"""

import os
import requests
import json

class WatsonxClient:
    def __init__(self, api_key=None, deployment_id=None, service_url=None):
        """
        Initialize Watsonx client.
        :param api_key: IBM Cloud API Key
        :param deployment_id: Watson Machine Learning Deployment ID
        :param service_url: IBM Cloud Region URL (e.g., https://us-south.ml.cloud.ibm.com)
        """
        self.api_key = api_key or os.getenv("IBM_CLOUD_API_KEY", "")
        self.deployment_id = deployment_id or os.getenv("WML_DEPLOYMENT_ID", "")
        self.service_url = (service_url or os.getenv("WML_SERVICE_URL", "https://us-south.ml.cloud.ibm.com")).rstrip('/')
        self.iam_url = "https://iam.cloud.ibm.com/identity/token"
        self._token = None

    def get_iam_token(self):
        """Exchange IBM Cloud API Key for IAM bearer token."""
        if not self.api_key:
            raise ValueError("IBM Cloud API Key not configured.")
        
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = f"apikey={self.api_key}&grant_type=urn:ibm:params:oauth:grant-type:apikey"
        
        response = requests.post(self.iam_url, headers=headers, data=data, timeout=10)
        if response.status_code != 200:
            raise Exception(f"IAM Token Generation failed [{response.status_code}]: {response.text}")
            
        token_data = response.json()
        self._token = token_data.get("access_token")
        return self._token

    def predict(self, fields, values):
        """
        Send online scoring payload to IBM Watson Machine Learning Deployment endpoint.
        
        :param fields: List of feature names, e.g. ['Glucose', 'BMI', ...]
        :param values: 2D list of feature values, e.g. [[148, 33.6, ...]]
        :return: dict with prediction result and class probabilities
        """
        if not self.api_key or not self.deployment_id:
            raise ValueError("IBM Cloud API Key or Deployment ID is missing.")

        token = self.get_iam_token()
        scoring_url = f"{self.service_url}/ml/v4/deployments/{self.deployment_id}/predictions?version=2021-05-01"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        payload = {
            "input_data": [{
                "fields": fields,
                "values": values
            }]
        }
        
        response = requests.post(scoring_url, headers=headers, json=payload, timeout=15)
        if response.status_code != 200:
            raise Exception(f"Watson scoring failed [{response.status_code}]: {response.text}")
            
        res_json = response.json()
        predictions = res_json.get("predictions", [{}])[0]
        pred_fields = predictions.get("fields", [])
        pred_values = predictions.get("values", [[]])[0]
        
        # Parse prediction output (e.g., [prediction, [prob_0, prob_1]])
        result = {}
        for idx, field in enumerate(pred_fields):
            if idx < len(pred_values):
                result[field] = pred_values[idx]
                
        return result
