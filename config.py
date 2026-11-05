"""
IBM watsonx.ai Studio & Cloud Configuration
Paste your IBM Cloud API Key and Project/Deployment details here.
"""

import os

# ==============================================================================
# PASTE YOUR IBM API KEY BELOW:
# Generated from IBM watsonx (Avatar -> Profile and settings -> API key -> Generate)
# OR from IBM Cloud (https://cloud.ibm.com -> Manage -> Access (IAM) -> API Keys)
# ==============================================================================
IBM_API_KEY = os.getenv("IBM_CLOUD_API_KEY", "")

# (Optional) Watson Machine Learning Deployment ID or Project ID
# Found in: Watson Studio -> Deployment Spaces -> Deployments tab
WATSONX_DEPLOYMENT_ID = os.getenv("WML_DEPLOYMENT_ID", "")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "")

# IBM Cloud Watson Service URL (Default: Dallas / us-south)
# Options depending on your IBM region:
#   - Dallas (us-south):     https://us-south.ml.cloud.ibm.com
#   - Frankfurt (eu-de):     https://eu-de.ml.cloud.ibm.com
#   - Tokyo (jp-tok):        https://jp-tok.ml.cloud.ibm.com
#   - London (eu-gb):        https://eu-gb.ml.cloud.ibm.com
WATSONX_URL = os.getenv("WML_SERVICE_URL", "https://us-south.ml.cloud.ibm.com")
