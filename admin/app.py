import sys
import os

# Robustly setup sys.path to prioritize root directory and avoid importing self as 'app'
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

# Insert parent dir at start
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Remove current dir from sys.path to prevent 'import app' from finding this script
if current_dir in sys.path:
    sys.path.remove(current_dir)

from app import create_app

app = create_app(register_blueprints=False)

from admin.routes import admin_bp
app.register_blueprint(admin_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
