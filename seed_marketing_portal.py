from app import create_app, db, MarketingUser
from werkzeug.security import generate_password_hash

def seed_marketing_user():
    app = create_app()
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if user already exists
        user = MarketingUser.query.filter_by(username='marketing_admin').first()
        if not user:
            new_user = MarketingUser(
                username='marketing_admin',
                email='marketing@teleportz.com',
                role='lead'
            )
            new_user.set_password('teleportz2026')
            db.session.add(new_user)
            db.session.commit()
            print("Marketing user created: marketing_admin / teleportz2026")
        else:
            print("Marketing user already exists.")

if __name__ == '__main__':
    seed_marketing_user()
