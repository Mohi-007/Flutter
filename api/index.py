import os
import sys

# In the root, the backend code is in the 'backend' folder
backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app import create_app

flask_app = create_app()
app = flask_app
