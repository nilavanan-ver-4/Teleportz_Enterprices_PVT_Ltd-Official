import sys
import os

# Add the directory containing botConnections to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Add the parent directory so we can import from the main app (db, models, Config)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the application factor from the botConnections/app.py
from app import app as application

# Set any environment variables if needed
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
