import os
import sys

# Ensure backend directory is in sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Ensure the root directory is in sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# Extend the 'api' package __path__ to include backend/api so that
# 'from api.routes import router' inside backend/main.py resolves correctly
import api
backend_api_dir = os.path.join(backend_dir, "api")
if hasattr(api, "__path__") and backend_api_dir not in api.__path__:
    api.__path__.append(backend_api_dir)

from main import app

# Expose app and application for Vercel ASGI
application = app
