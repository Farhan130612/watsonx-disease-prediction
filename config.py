"""
IBM watsonx.ai Studio & Cloud Configuration
Paste your IBM Cloud API Key and Project/Deployment details here.
"""

import os

# ==============================================================================
# IBM CLOUD / WATSONX CREDENTIALS
# ==============================================================================
IBM_API_KEY = os.getenv("IBM_CLOUD_API_KEY", "1lG7yyuGHBBwpGdFpzec5riGiMQeOOe_nhi15nL0ae-r")

# Watson Machine Learning Project & Deployment
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "7b994633-6cb7-4e25-9b7b-26d8ee076a8f")
WATSONX_DEPLOYMENT_ID = os.getenv("WML_DEPLOYMENT_ID", "")
WATSONX_SPACE_ID = os.getenv("WATSONX_SPACE_ID", "78f2681d-e214-4452-a3b8-a7217f62692a")

# IBM Cloud Watson Service URL
WATSONX_URL = os.getenv("WML_SERVICE_URL", "https://au-syd.dai.cloud.ibm.com")
