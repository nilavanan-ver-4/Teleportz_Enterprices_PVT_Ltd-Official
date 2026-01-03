from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, send_from_directory, current_app
from app import Product, Inquiry, db
from sqlalchemy import or_
import os

official_bp = Blueprint('official', __name__, template_folder='templates', static_folder='static', static_url_path='/official/static')


@official_bp.route('/')
def home():
    products = Product.query.filter(Product.id.in_([1, 5])).all()
    return render_template('official/home.html', products=products)

@official_bp.route('/about')
def about():
    return render_template('official/about.html')

@official_bp.route('/services')
def services():
    return render_template('official/services.html')

@official_bp.route('/products')
def products():
    # If DB has no products yet, seed it with the provided PRODUCTS_DATA
    if Product.query.count() == 0:
        for p in PRODUCTS_DATA:
            prod = Product(
                name=p['name'],
                category=p['category'],
                description=p['description'],
                image_filename=p.get('image_filename') or None
            )
            db.session.add(prod)
        db.session.commit()

    search = request.args.get('search', '').strip()

    # Basic search across name, category, and description (case-insensitive)
    query = Product.query
    if search:
        query = query.filter(or_(Product.name.ilike(f'%{search}%'),
                                 Product.category.ilike(f'%{search}%'),
                                 Product.description.ilike(f'%{search}%')))

    products = query.order_by(Product.created_at.desc()).all()
    return render_template('official/products.html', products=products, search=search)


@official_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded product images from the instance folder."""
    upload_path = os.path.join(current_app.instance_path, 'uploads')
    return send_from_directory(upload_path, filename)


@official_bp.route('/api/products')
def api_products():
    """Return product list as JSON for AJAX search (limits to 50 results)."""
    search = request.args.get('search', '').strip()
    query = Product.query
    if search:
        query = query.filter(or_(Product.name.ilike(f'%{search}%'),
                                 Product.category.ilike(f'%{search}%'),
                                 Product.description.ilike(f'%{search}%')))

    products = query.order_by(Product.created_at.desc()).limit(50).all()

    results = []
    for p in products:
        img = None
        if p.image_filename:
            img = url_for('official.uploaded_file', filename=p.image_filename)
        results.append({
            'id': p.id,
            'name': p.name,
            'category': p.category,
            'description': p.description,
            'image_url': img
        })

    return jsonify(results)

@official_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        if name and email and message:
            new_inquiry = Inquiry(name=name, email=email, subject=subject, message=message)
            db.session.add(new_inquiry)
            db.session.commit()
            flash('Your message has been sent successfully! We will contact you soon.', 'success')
            return redirect(url_for('official.contact'))
        else:
            flash('Please fill in all required fields.', 'danger')
            
    return render_template('official/contact.html')

@official_bp.route('/privacy')
def privacy():
    return render_template('official/privacy.html')

@official_bp.route('/terms')
def terms():
    return render_template('official/terms.html')
