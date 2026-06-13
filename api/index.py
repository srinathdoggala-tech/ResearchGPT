import sys
import os

# Add the backend directory to the Python path so Vercel can locate config, main, etc.
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from main import app
