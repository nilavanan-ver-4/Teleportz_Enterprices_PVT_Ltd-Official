import os
import sys
import traceback

# Add career directory to path to import models directly
current_dir = os.path.dirname(os.path.abspath(__file__))
career_dir = os.path.join(current_dir, 'career')
if career_dir not in sys.path:
    sys.path.insert(0, career_dir)

try:
    from app import create_app
    from models import db, CareerUser, Job, JobApplication, ApplicationTracking
    
    app = create_app()
    with app.app_context():
        db.create_all()
        user = CareerUser.query.filter_by(phone='+91 99999 99999').first()
        print("Success!")
except Exception:
    traceback.print_exc()
