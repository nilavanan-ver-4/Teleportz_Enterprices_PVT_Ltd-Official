from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class CareerUser(db.Model, UserMixin):
    __tablename__ = 'career_user'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    otp = db.Column(db.String(6))
    otp_expiry = db.Column(db.DateTime)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Profile Information
    full_name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    experience_summary = db.Column(db.Text)
    education = db.Column(db.Text)
    skills = db.Column(db.Text)
    resume_path = db.Column(db.String(255))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    experience = db.Column(db.String(100), nullable=False)
    salary_range = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    benefits = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('career_user.id'), nullable=True)
    
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)
    cover_letter = db.Column(db.Text)
    resume_filename = db.Column(db.String(255))
    photo_filename = db.Column(db.String(255))
    status = db.Column(db.String(50), default='pending') # pending, reviewing, shortlisted, interviewed, rejected, hired
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    job = db.relationship('Job', backref=db.backref('applications', lazy=True))
    user = db.relationship('CareerUser', backref=db.backref('applications', lazy=True))

class ApplicationTracking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('job_application.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    
    application = db.relationship('JobApplication', backref=db.backref('tracking_records', lazy=True, order_by='ApplicationTracking.update_time.desc()'))