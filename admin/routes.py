from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import User, Product, Inquiry, db

import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin', __name__, template_folder='templates', static_folder='static', static_url_path='/admin/static')

# Helpers
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# Auth Routes
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('admin.login'))

# Dashboard
@admin_bp.route('/')
@login_required
def dashboard():
    product_count = Product.query.count()
    inquiry_count = Inquiry.query.count()
    unread_inquiries = Inquiry.query.filter_by(is_read=False).count()
    recent_inquiries = Inquiry.query.order_by(Inquiry.received_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', 
                           product_count=product_count, 
                           inquiry_count=inquiry_count, 
                           unread_inquiries=unread_inquiries,
                           recent_inquiries=recent_inquiries)

# Product Management
@admin_bp.route('/products')
@login_required
def products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin/products.html', products=products)

@admin_bp.route('/products/new', methods=['GET', 'POST'])
@login_required
def new_product():
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        description = request.form.get('description')
        file = request.files.get('image')
        
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Ensure upload folder exists
            upload_path = os.path.join(current_app.instance_path, 'uploads')
            os.makedirs(upload_path, exist_ok=True)
            file.save(os.path.join(upload_path, filename))
        
        product = Product(name=name, category=category, description=description, image_filename=filename)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('admin.products'))
        
    return render_template('admin/product_form.html', action='New')

@admin_bp.route('/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.category = request.form.get('category')
        product.description = request.form.get('description')
        file = request.files.get('image')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.instance_path, 'uploads')
            os.makedirs(upload_path, exist_ok=True)
            file.save(os.path.join(upload_path, filename))
            product.image_filename = filename
            
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('admin.products'))
        
    return render_template('admin/product_form.html', product=product, action='Edit')

@admin_bp.route('/products/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted.', 'info')
    return redirect(url_for('admin.products'))

# Inquiries
@admin_bp.route('/inquiries')
@login_required
def inquiries():
    inquiries = Inquiry.query.order_by(Inquiry.received_at.desc()).all()
    return render_template('admin/inquiries.html', inquiries=inquiries)

@admin_bp.route('/inquiries/<int:id>')
@login_required
def view_inquiry(id):
    inquiry = Inquiry.query.get_or_404(id)
    if not inquiry.is_read:
        inquiry.is_read = True
        db.session.commit()
    return render_template('admin/inquiry_detail.html', inquiry=inquiry)
