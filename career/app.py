import os
import sys
from flask import Flask
from flask_login import LoginManager
from models import db, CareerUser

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'teleportz-career-secret-high-tech'
    app.config['SESSION_COOKIE_NAME'] = 'teleportz_career_session'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(parent_dir, "database", "site.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'career.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(CareerUser, int(user_id))
    
    from routes import career_bp
    app.register_blueprint(career_bp)
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5002)