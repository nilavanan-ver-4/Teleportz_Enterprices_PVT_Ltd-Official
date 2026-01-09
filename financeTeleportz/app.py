import os
import sys
from flask import Flask
from flask_login import LoginManager

# Add parent directory to path to reach root app.py models and config
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app import db, FinanceUser, Config

def create_finance_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Ensure relative paths for database work if running standalone
    if not app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite:///'):
         basedir = os.path.abspath(os.path.join(current_dir, '..'))
         app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database', 'site.db')

    app.config['SESSION_COOKIE_NAME'] = 'finance_teleportz_standalone_session'
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'finance.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(FinanceUser, int(user_id))
    
    from routes import finance_bp
    app.register_blueprint(finance_bp, url_prefix='')
    
    return app

app = create_finance_app()

if __name__ == '__main__':
    app.run(debug=True, port=5006)
