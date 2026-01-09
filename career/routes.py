from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory, current_app
from models import Job, JobApplication, ApplicationTracking, CareerUser, db
from werkzeug.utils import secure_filename
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
import os
import uuid
import random

career_bp = Blueprint('career', __name__, template_folder='templates', static_folder='static')

def send_mock_otp(phone, otp):
    # In a real app, this would use Twilio or similar
    print(f"DEBUG: OTP for {phone} is {otp}")
    return True

@career_bp.route('/')
def careers():
    jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).all()
    return render_template('career/careers.html', jobs=jobs)

@career_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('career.careers'))
        
    if request.method == 'POST':
        phone = request.form.get('phone')
        if not phone:
            flash('Please enter your mobile number.', 'danger')
            return render_template('career/login.html')
            
        # Check if user exists or create new
        user = CareerUser.query.filter_by(phone=phone).first()
        if not user:
            user = CareerUser(phone=phone)
            db.session.add(user)
            db.session.commit()
            
        # Generate OTP
        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.otp_expiry = datetime.utcnow() + timedelta(minutes=5)
        db.session.commit()
        
        send_mock_otp(phone, otp)
        flash(f'OTP sent to {phone}. (Use {otp} for testing)', 'success')
        return redirect(url_for('career.verify_otp', phone=phone))
        
    return render_template('career/login.html')

@career_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    phone = request.args.get('phone')
    if not phone:
        return redirect(url_for('career.login'))
        
    if request.method == 'POST':
        otp_entered = request.form.get('otp')
        user = CareerUser.query.filter_by(phone=phone).first()
        
        if user and user.otp == otp_entered and user.otp_expiry > datetime.utcnow():
            user.is_verified = True
            user.otp = None
            db.session.commit()
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('career.profile'))
        else:
            flash('Invalid or expired OTP.', 'danger')
            
    return render_template('career/verify_otp.html', phone=phone)

@career_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('career.careers'))

@career_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name')
        current_user.email = request.form.get('email')
        current_user.experience_summary = request.form.get('experience_summary')
        current_user.education = request.form.get('education')
        current_user.skills = request.form.get('skills')
        
        # Handle Resume Upload
        if 'resume' in request.files:
            resume_file = request.files['resume']
            if resume_file and resume_file.filename:
                os.makedirs(os.path.join(current_app.instance_path, 'uploads', 'resumes'), exist_ok=True)
                filename = secure_filename(resume_file.filename)
                unique_filename = f"user_{current_user.id}_{uuid.uuid4()}_{filename}"
                resume_path = os.path.join(current_app.instance_path, 'uploads', 'resumes', unique_filename)
                resume_file.save(resume_path)
                current_user.resume_path = unique_filename
                
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        
    return render_template('career/profile.html', user=current_user)

@career_bp.route('/job/<int:job_id>')
def job_detail(job_id):
    job = db.get_or_404(Job, job_id)
    if not job.is_active:
        flash('This job posting is no longer available.', 'info')
        return redirect(url_for('career.careers'))
    return render_template('career/job_detail.html', job=job)

@career_bp.route('/job/<int:job_id>/apply', methods=['GET', 'POST'])
def apply_job(job_id):
    job = db.get_or_404(Job, job_id)
    if not job.is_active:
        flash('This job posting is no longer available.', 'info')
        return redirect(url_for('career.careers'))
    
    if request.method == 'POST':
        # If logged in, use profile info
        if current_user.is_authenticated:
            name = current_user.full_name or "Anonymous"
            email = current_user.email or "N/A"
            phone = current_user.phone
        else:
            name = request.form.get('name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            
        experience_years = request.form.get('experience_years')
        cover_letter = request.form.get('cover_letter')
        
        if not all([name, email, phone, experience_years]):
            flash('Please fill in all required fields.', 'danger')
            return render_template('career/apply_job.html', job=job)
        
        # Handle file uploads
        resume_filename = current_user.resume_path if current_user.is_authenticated else None
        photo_filename = None
        
        uploads_dir = os.path.join(current_app.instance_path, 'uploads')
        os.makedirs(os.path.join(uploads_dir, 'resumes'), exist_ok=True)
        os.makedirs(os.path.join(uploads_dir, 'photos'), exist_ok=True)
        
        if 'resume' in request.files and request.files['resume'].filename:
            resume_file = request.files['resume']
            filename = secure_filename(resume_file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            resume_file.save(os.path.join(uploads_dir, 'resumes', unique_filename))
            resume_filename = unique_filename
        
        if 'photo' in request.files and request.files['photo'].filename:
            photo_file = request.files['photo']
            filename = secure_filename(photo_file.filename)
            unique_filename = f"{uuid.uuid4()}_{filename}"
            photo_file.save(os.path.join(uploads_dir, 'photos', unique_filename))
            photo_filename = unique_filename
        
        # Create job application
        application = JobApplication(
            job_id=job_id,
            user_id=current_user.id if current_user.is_authenticated else None,
            name=name,
            email=email,
            phone=phone,
            experience_years=int(experience_years),
            cover_letter=cover_letter,
            resume_filename=resume_filename,
            photo_filename=photo_filename
        )
        
        db.session.add(application)
        db.session.flush() # Get application ID
        
        # Add initial tracking record
        tracking = ApplicationTracking(
            application_id=application.id,
            status='Applied',
            notes='Application submitted successfully through portal.'
        )
        db.session.add(tracking)
        db.session.commit()
        
        flash('Your application has been submitted successfully! You can track its status in your profile.', 'success')
        return redirect(url_for('career.my_applications') if current_user.is_authenticated else url_for('career.careers'))
    
    return render_template('career/apply_job.html', job=job)

@career_bp.route('/my-applications')
@login_required
def my_applications():
    applications = JobApplication.query.filter_by(user_id=current_user.id).order_by(JobApplication.applied_at.desc()).all()
    return render_template('career/my_applications.html', applications=applications)

@career_bp.route('/uploads/resumes/<filename>')
def resume_file(filename):
    resumes_path = os.path.join(current_app.instance_path, 'uploads', 'resumes')
    return send_from_directory(resumes_path, filename)

@career_bp.route('/uploads/photos/<filename>')
def photo_file(filename):
    photos_path = os.path.join(current_app.instance_path, 'uploads', 'photos')
    return send_from_directory(photos_path, filename)