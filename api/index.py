"""
Vercel Serverless Function entrypoint for CardioDiab-AI Flask Application.
Includes WSGI path resolver to prevent 404 Not Found on Vercel rewrites.
"""

import os
import sys

# Add project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app import app

class VercelPathMiddleware:
    """
    Normalizes Vercel's rewritten PATH_INFO so Flask routes match seamlessly.
    Handles /api/index, /api/index.py, and preserves sub-paths.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        # Check if Vercel set original matched path header
        orig_path = (
            environ.get('HTTP_X_MATCHED_PATH') or 
            environ.get('HTTP_X_NOW_ROUTE_MATCHES') or 
            environ.get('HTTP_X_FORWARDED_URI')
        )
        if orig_path:
            environ['PATH_INFO'] = orig_path
        elif path == '/api/index' or path == '/api/index.py' or path == '/api/index/':
            environ['PATH_INFO'] = '/'
        elif path.startswith('/api/index/'):
            environ['PATH_INFO'] = path[len('/api/index'):]

        return self.wsgi_app(environ, start_response)

# Export WSGI application wrapped with middleware
app = VercelPathMiddleware(app)
