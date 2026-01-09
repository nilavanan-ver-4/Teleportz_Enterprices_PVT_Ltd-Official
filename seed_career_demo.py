import os
import sys
from datetime import datetime, timedelta

# Add career directory to path to import models directly
current_dir = os.path.dirname(os.path.abspath(__file__))
career_dir = os.path.join(current_dir, 'career')
if career_dir not in sys.path:
    sys.path.insert(0, career_dir)

from app import create_app
from models import db, CareerUser, Job, JobApplication, ApplicationTracking

def seed_career_data():
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # --- Diverse Job Postings ---
        more_jobs = [
            {
                'title': 'AI & Machine Learning Engineer',
                'department': 'Engineering',
                'location': 'Bangalore, India (Remote Friendly)',
                'type': 'Full-time',
                'experience': '3-5 Years',
                'description': 'Develop AI-driven trade intelligence models and predictive supply chain analytics.',
                'requirements': 'MS/PhD in CS/AI, experience with PyTorch/TensorFlow, and large-scale data processing.',
                'is_active': True
            },
            {
                'title': 'Robotics Software Developer (Warehouse Automation)',
                'department': 'Robotics',
                'location': 'Chennai, India',
                'type': 'Full-time',
                'experience': '2-4 Years',
                'description': 'Building next-gen autonomous mobile robots for international warehousing solutions.',
                'requirements': 'Expertise in ROS, C++, and Path Planning algorithms.',
                'is_active': True
            },
            {
                'title': 'Cloud Infrastructure Architect',
                'department': 'IT Infrastructure',
                'location': 'Chennai, India',
                'type': 'Full-time',
                'experience': '5-8 Years',
                'description': 'Design secure and scalable global cloud infrastructure for Teleportz trade platforms.',
                'requirements': 'AWS/Azure certification, Kubernetes, and Terraform expertise.',
                'is_active': True
            },
            {
                'title': 'Senior Data Scientist (Global Trade)',
                'department': 'Data Analytics',
                'location': 'Remote / Mumbai',
                'type': 'Full-time',
                'experience': '4-6 Years',
                'description': 'Analyze global trade patterns and optimize route efficiency using data-driven insights.',
                'requirements': 'Strong statistical background, SQL, Python, and experience with logistics data.',
                'is_active': True
            }
        ]

        for job_data in more_jobs:
            existing_job = Job.query.filter_by(title=job_data['title']).first()
            if not existing_job:
                new_job = Job(**job_data)
                db.session.add(new_job)

        db.session.commit()

        # Ensure original demo job exists
        job = Job.query.filter_by(title='Global Supply Chain Associate').first()
        if not job:
            job = Job(
                title='Global Supply Chain Associate',
                department='Logistics',
                location='Chennai, India',
                type='Full-time',
                experience='2-4 Years',
                description='Manage international vendor relationships and supply chain logistics.',
                requirements='Degree in Logistics or Supply Chain Management.',
                is_active=True
            )
            db.session.add(job)
            db.session.commit()

        # Create a demo user
        user = CareerUser.query.filter_by(phone='+91 99999 99999').first()
        if not user:
            user = CareerUser(
                phone='+91 99999 99999',
                full_name='Demo Candidate',
                email='demo@teleportz.com',
                experience_summary='Experienced supply chain professional with 3 years in EXIM.',
                is_verified=True
            )
            db.session.add(user)
            db.session.commit()

        # Create/Update an application for the demo user
        application = JobApplication.query.filter_by(user_id=user.id, job_id=job.id).first()
        if not application:
            application = JobApplication(
                job_id=job.id,
                user_id=user.id,
                name=user.full_name,
                email=user.email,
                phone=user.phone,
                experience_years=3,
                status='shortlisted'
            )
            db.session.add(application)
            db.session.flush()

        # Add tracking records
        ApplicationTracking.query.filter_by(application_id=application.id).delete()
        
        records = [
            ('Applied', 'Application received and registered in global database.', -3),
            ('Reviewing', 'Resume parsed and initial verification by HR Compliance.', -2),
            ('Assessment', 'Online technical assessment completed with 92% score.', -1),
            ('Shortlisted', 'Shortlisted for Leadership Interview. Schedule pending.', 0)
        ]

        for status, notes, days_ago in records:
            update_time = datetime.utcnow() + timedelta(days=days_ago)
            tracking = ApplicationTracking(
                application_id=application.id,
                status=status,
                notes=notes,
                update_time=update_time
            )
            db.session.add(tracking)

        db.session.commit()
        print("Career data (including diverse jobs) seeded successfully!")

if __name__ == '__main__':
    seed_career_data()
