"""
Vercel Serverless Function entrypoint for CardioDiab-AI Flask Application.
"""

import os
import sys

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import app

# Vercel WSGI entrypoint
app = app
