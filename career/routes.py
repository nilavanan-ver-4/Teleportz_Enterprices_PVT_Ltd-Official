from flask import Blueprint, render_template, request, flash, redirect, url_for, send_from_directory, current_app
from models import Job, JobApplication, db
from werkzeug.utils import secure_filename
import os
import uuid

career_bp = Blueprint('career', __name__, template_folder='templates', static_folder='static')

@career_bp.route('/')
def careers():
    jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).all()
    return render_template('career/careers.html', jobs=jobs)

@career_bp.route('/job/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    if not job.is_active:
        flash('This job posting is no longer available.', 'info')
        return redirect(url_for('career.careers'))
    return render_template('career/job_detail.html', job=job)

@career_bp.route('/job/<int:job_id>/apply', methods=['GET', 'POST'])
def apply_job(job_id):
    job = Job.query.get_or_404(job_id)
    if not job.is_active:
        flash('This job posting is no longer available.', 'info')
        return redirect(url_for('career.careers'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        experience_years = request.form.get('experience_years')
        cover_letter = request.form.get('cover_letter')
        
        if not all([name, email, phone, experience_years]):
            flash('Please fill in all required fields.', 'danger')
            return render_template('career/apply_job.html', job=job)
        
        # Handle file uploads
        resume_filename = None
        photo_filename = None
        
        # Create uploads directory if it doesn't exist
        uploads_dir = os.path.join(current_app.instance_path, 'uploads')
        resumes_dir = os.path.join(uploads_dir, 'resumes')
        photos_dir = os.path.join(uploads_dir, 'photos')
        
        os.makedirs(resumes_dir, exist_ok=True)
        os.makedirs(photos_dir, exist_ok=True)
        
        if 'resume' in request.files:
            resume_file = request.files['resume']
            if resume_file and resume_file.filename:
                filename = secure_filename(resume_file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                resume_path = os.path.join(resumes_dir, unique_filename)
                resume_file.save(resume_path)
                resume_filename = unique_filename
        
        if 'photo' in request.files:
            photo_file = request.files['photo']
            if photo_file and photo_file.filename:
                filename = secure_filename(photo_file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                photo_path = os.path.join(photos_dir, unique_filename)
                photo_file.save(photo_path)
                photo_filename = unique_filename
        
        # Create job application
        application = JobApplication(
            job_id=job_id,
            name=name,
            email=email,
            phone=phone,
            experience_years=int(experience_years),
            cover_letter=cover_letter,
            resume_filename=resume_filename,
            photo_filename=photo_filename
        )
        
        db.session.add(application)
        db.session.commit()
        
        flash('Your application has been submitted successfully! We will contact you soon.', 'success')
        return redirect(url_for('career.job_detail', job_id=job_id))
    
    return render_template('career/apply_job.html', job=job)

@career_bp.route('/uploads/resumes/<filename>')
def resume_file(filename):
    resumes_path = os.path.join(current_app.instance_path, 'uploads', 'resumes')
    return send_from_directory(resumes_path, filename)

@career_bp.route('/uploads/photos/<filename>')
def photo_file(filename):
    photos_path = os.path.join(current_app.instance_path, 'uploads', 'photos')
    return send_from_directory(photos_path, filename)