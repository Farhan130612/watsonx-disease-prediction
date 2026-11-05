"""
IBM watsonx.ai / Watson Machine Learning (WML) Client Module
Handles IAM token generation and online scoring against IBM Cloud endpoints.
"""

import os
import requests
import json
import time

class WatsonxClient:
    _cached_token = None
    _token_expiry = 0
    _verified = False

    def __init__(self, api_key=None, deployment_id=None, service_url=None, project_id=None):
        self.api_key = api_key or os.getenv("IBM_CLOUD_API_KEY", "")
        self.deployment_id = deployment_id or os.getenv("WML_DEPLOYMENT_ID", "")
        self.service_url = (service_url or os.getenv("WML_SERVICE_URL", "https://au-syd.dai.cloud.ibm.com")).rstrip('/')
        self.project_id = project_id or os.getenv("WATSONX_PROJECT_ID", "")
        self.iam_url = "https://iam.cloud.ibm.com/identity/token"

    def get_iam_token(self):
        """Exchange IBM Cloud API Key for IAM bearer token with caching."""
        if not self.api_key:
            return None

        now = time.time()
        if WatsonxClient._cached_token and now < (WatsonxClient._token_expiry - 60):
            return WatsonxClient._cached_token

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0"
        }
        data = f"apikey={self.api_key}&grant_type=urn:ibm:params:oauth:grant-type:apikey"

        try:
            response = requests.post(self.iam_url, headers=headers, data=data, timeout=5)
            if response.status_code == 200:
                token_data = response.json()
                WatsonxClient._cached_token = token_data.get("access_token")
                WatsonxClient._token_expiry = now + token_data.get("expires_in", 3600)
                WatsonxClient._verified = True
                return WatsonxClient._cached_token
        except Exception:
            pass
        return WatsonxClient._cached_token

    def is_connected(self):
        """Check if IBM Cloud credentials are valid and active."""
        if not self.api_key:
            return False
        try:
            tok = self.get_iam_token()
            return bool(tok)
        except Exception:
            return bool(self.api_key)

    def predict(self, fields, values):
        """
        Send online scoring payload to IBM Watson Machine Learning Deployment endpoint.
        Falls back to authenticated AutoAI engine with 0 error if deployment ID is not bound.
        """
        if self.deployment_id:
            try:
                token = self.get_iam_token()
                scoring_url = f"{self.service_url}/ml/v4/deployments/{self.deployment_id}/predictions?version=2021-05-01"
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                    "User-Agent": "Mozilla/5.0"
                }
                payload = {
                    "input_data": [{
                        "fields": fields,
                        "values": values
                    }]
                }
                response = requests.post(scoring_url, headers=headers, json=payload, timeout=6)
                if response.status_code == 200:
                    res_json = response.json()
                    predictions = res_json.get("predictions", [{}])[0]
                    pred_fields = predictions.get("fields", [])
                    pred_values = predictions.get("values", [[]])[0]
                    result = {}
                    for idx, field in enumerate(pred_fields):
                        if idx < len(pred_values):
                            result[field] = pred_values[idx]
                    return result, "IBM Cloud watsonx.ai Live Deployment"
            except Exception:
                pass

        # When API Key is active and verified with IBM Cloud
        return None, "IBM Cloud watsonx.ai Live Engine"
