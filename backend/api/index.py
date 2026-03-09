import os
import sys

# Ensure the backend directory is in the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from app import create_app

flask_app = create_app()
app = flask_app
