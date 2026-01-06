from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, send_from_directory, current_app
from app import Product, Inquiry, Job, JobApplication, db
from sqlalchemy import or_
from werkzeug.utils import secure_filename
import os
import uuid

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

@official_bp.route('/services/<slug>')
def service_detail(slug):
    services_data = {
        'import-services': {
            'name': 'Import Services',
            'desc': 'Seamlessly bring quality global products to your doorstep',
            'icon': 'fa-ship',
            'full_desc': 'Our comprehensive import services help you source quality products from around the world with complete compliance and documentation support.',
            'features': ['Global sourcing of quality products', 'Vendor verification and compliance', 'Customs coordination support', 'Import duty optimization']
        },
        'export-services': {
            'name': 'Export Services',
            'desc': 'Expand your business globally with our export solutions',
            'icon': 'fa-plane-departure',
            'full_desc': 'We handle all aspects of international product distribution, from documentation to logistics coordination.',
            'features': ['International product distribution', 'Documentation assistance', 'Logistics coordination', 'Market entry support']
        },
        'logistics-supply-chain': {
            'name': 'Logistics & Supply Chain',
            'desc': 'Efficient freight and supply chain management',
            'icon': 'fa-truck-fast',
            'full_desc': 'Optimize your supply chain with our freight coordination and logistics planning services.',
            'features': ['Freight coordination (air, sea, land)', 'Shipment tracking and scheduling', 'Cost-effective logistics planning', 'Real-time visibility']
        },
        'documentation-regulatory': {
            'name': 'Documentation & Regulatory',
            'desc': 'Complete compliance and regulatory support',
            'icon': 'fa-file-signature',
            'full_desc': 'Navigate complex international trade regulations with our expert documentation and compliance guidance.',
            'features': ['Export-import documentation', 'Customs coordination', 'HS code & compliance guidance', 'Regulatory compliance']
        },
        'trade-consulting': {
            'name': 'Trade Consulting',
            'desc': 'Strategic guidance for global trade',
            'icon': 'fa-briefcase',
            'full_desc': 'Get expert advice on market entry, supplier connections, and risk mitigation strategies.',
            'features': ['Market entry guidance', 'Supplier & buyer connections', 'Risk mitigation strategies', 'Trade strategy development']
        },
        'quality-compliance': {
            'name': 'Quality & Compliance',
            'desc': 'Ensure product quality and international standards',
            'icon': 'fa-clipboard-check',
            'full_desc': 'Maintain the highest quality standards with our comprehensive quality checks and compliance audits.',
            'features': ['Product quality checks', 'International trade standards', 'Factory audits & inspections', 'Certification support']
        },
        'post-shipment-support': {
            'name': 'Post-Shipment Support',
            'desc': 'Continuous support after delivery',
            'icon': 'fa-headset',
            'full_desc': 'We provide ongoing support to ensure smooth delivery and resolution of any post-shipment issues.',
            'features': ['Shipment follow-ups', 'Issue resolution & coordination', 'Long-term client assistance', 'Customer support']
        },
        'custom-trade-solutions': {
            'name': 'Custom Trade Solutions',
            'desc': 'Tailored solutions for your unique needs',
            'icon': 'fa-sliders',
            'full_desc': 'We create customized trade solutions designed specifically for your industry and business requirements.',
            'features': ['Industry-specific sourcing', 'Custom order handling', 'Flexible trade models', 'Bespoke solutions']
        }
    }
    
    service = services_data.get(slug)
    if not service:
        return redirect(url_for('official.services'))
    
    return render_template('official/services_detail.html',
                         service_name=service['name'],
                         service_desc=service['desc'],
                         service_icon=service['icon'],
                         service_full_desc=service['full_desc'],
                         service_features=service['features'])

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
    """Serve uploaded product images from the database folder."""
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

@official_bp.route('/policy')
def policy():
    return render_template('official/policy.html')

@official_bp.route('/features')
def features():
    features_data = [
        {'slug': 'trade-intelligence', 'title': 'Global Trade Intelligence', 'summary': 'Real-time insights into global trade patterns', 'icon': 'fa-brain'},
        {'slug': 'buyers-intelligence', 'title': 'Buyers Intelligence', 'summary': 'Identify and connect with qualified buyers', 'icon': 'fa-user-tag'},
        {'slug': 'suppliers-intelligence', 'title': 'Suppliers Intelligence', 'summary': 'Discover reliable suppliers worldwide', 'icon': 'fa-industry'},
        {'slug': 'market-intelligence', 'title': 'Market Intelligence', 'summary': 'Deep insights into market dynamics', 'icon': 'fa-chart-line'},
        {'slug': 'trade-platform', 'title': 'Trade Platform', 'summary': 'All-in-one platform for trade management', 'icon': 'fa-laptop-code'},
        {'slug': 'competitive-intel', 'title': 'Competitive Intel', 'summary': 'Stay ahead of competition', 'icon': 'fa-bolt'},
        {'slug': 'product-intel', 'title': 'Product Intel', 'summary': 'Detailed product market analysis', 'icon': 'fa-box'},
        {'slug': 'supply-chain-intel', 'title': 'Supply Chain Intel', 'summary': 'Optimize your supply chain network', 'icon': 'fa-link'}
    ]
    return render_template('official/features/index.html', features=features_data)

@official_bp.route('/careers')
def careers():
    jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).all()
    return render_template('official/careers.html', jobs=jobs)

@official_bp.route('/careers/<int:job_id>')
def job_detail(job_id):
    job = Job.query.get_or_404(job_id)
    if not job.is_active:
        flash('This job posting is no longer available.', 'info')
        return redirect(url_for('official.careers'))
    return render_template('official/job_detail.html', job=job)

@official_bp.route('/careers/<int:job_id>/apply', methods=['GET', 'POST'])
def apply_job(job_id):
    job = Job.query.get_or_404(job_id)
    if not job.is_active:
        flash('This job posting is no longer available.', 'info')
        return redirect(url_for('official.careers'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        experience_years = request.form.get('experience_years')
        cover_letter = request.form.get('cover_letter')
        
        if not all([name, email, phone, experience_years]):
            flash('Please fill in all required fields.', 'danger')
            return render_template('official/apply_job.html', job=job)
        
        # Handle file uploads
        resume_filename = None
        photo_filename = None
        
        if 'resume' in request.files:
            resume_file = request.files['resume']
            if resume_file and resume_file.filename:
                filename = secure_filename(resume_file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                resume_path = os.path.join(current_app.instance_path, 'uploads', 'resumes', unique_filename)
                resume_file.save(resume_path)
                resume_filename = unique_filename
        
        if 'photo' in request.files:
            photo_file = request.files['photo']
            if photo_file and photo_file.filename:
                filename = secure_filename(photo_file.filename)
                unique_filename = f"{uuid.uuid4()}_{filename}"
                photo_path = os.path.join(current_app.instance_path, 'uploads', 'photos', unique_filename)
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
        return redirect(url_for('official.job_detail', job_id=job_id))
    
    return render_template('official/apply_job.html', job=job)

@official_bp.route('/uploads/resumes/<filename>')
def resume_file(filename):
    """Serve resume files from the resumes folder."""
    resumes_path = os.path.join(current_app.instance_path, 'uploads', 'resumes')
    return send_from_directory(resumes_path, filename)

@official_bp.route('/uploads/photos/<filename>')
def photo_file(filename):
    """Serve photo files from the photos folder."""
    photos_path = os.path.join(current_app.instance_path, 'uploads', 'photos')
    return send_from_directory(photos_path, filename)

@official_bp.route('/features/<slug>')
def feature_detail(slug):
    features_data = {
        'trade-intelligence': {
            'name': 'Global Trade Intelligence',
            'desc': 'Real-time insights into global trade patterns',
            'icon': 'fa-brain',
            'full_desc': 'Access comprehensive trade data and market intelligence to make informed business decisions.',
            'benefits': ['Real-time trade data', 'Market trend analysis', 'Competitor insights', 'Trade opportunity identification']
        },
        'buyers-intelligence': {
            'name': 'Buyers Intelligence',
            'desc': 'Identify and connect with qualified buyers',
            'icon': 'fa-user-tag',
            'full_desc': 'Find and analyze potential buyers in your target markets with detailed buyer profiles.',
            'benefits': ['Buyer database access', 'Buyer profiling', 'Contact information', 'Purchase history analysis']
        },
        'suppliers-intelligence': {
            'name': 'Suppliers Intelligence',
            'desc': 'Discover reliable suppliers worldwide',
            'icon': 'fa-industry',
            'full_desc': 'Access verified supplier information and ratings to find the best partners for your business.',
            'benefits': ['Supplier verification', 'Quality ratings', 'Pricing comparison', 'Supplier reliability scores']
        },
        'market-intelligence': {
            'name': 'Market Intelligence',
            'desc': 'Deep insights into market dynamics',
            'icon': 'fa-chart-line',
            'full_desc': 'Understand market trends, demand patterns, and competitive landscape in your industry.',
            'benefits': ['Market size analysis', 'Growth trends', 'Demand forecasting', 'Competitive analysis']
        },
        'trade-platform': {
            'name': 'Trade Platform',
            'desc': 'All-in-one platform for trade management',
            'icon': 'fa-laptop-code',
            'full_desc': 'Manage all your trade operations from a single integrated platform.',
            'benefits': ['Order management', 'Document handling', 'Payment processing', 'Shipment tracking']
        },
        'competitive-intel': {
            'name': 'Competitive Intel',
            'desc': 'Stay ahead of competition',
            'icon': 'fa-bolt',
            'full_desc': 'Monitor competitor activities and market positioning to maintain competitive advantage.',
            'benefits': ['Competitor monitoring', 'Price tracking', 'Strategy analysis', 'Market positioning']
        },
        'product-intel': {
            'name': 'Product Intel',
            'desc': 'Detailed product market analysis',
            'icon': 'fa-box',
            'full_desc': 'Get comprehensive insights on product performance, demand, and market opportunities.',
            'benefits': ['Product demand analysis', 'Price trends', 'Quality benchmarking', 'Market opportunities']
        },
        'supply-chain-intel': {
            'name': 'Supply Chain Intel',
            'desc': 'Optimize your supply chain network',
            'icon': 'fa-link',
            'full_desc': 'Analyze and optimize your supply chain for efficiency and cost reduction.',
            'benefits': ['Supply chain mapping', 'Cost optimization', 'Risk assessment', 'Efficiency improvement']
        }
    }
    
    feature = features_data.get(slug)
    if not feature:
        return redirect(url_for('official.products'))
    
    return render_template('official/features_detail.html',
                         feature_name=feature['name'],
                         feature_desc=feature['desc'],
                         feature_icon=feature['icon'],
                         feature_full_desc=feature['full_desc'],
                         feature_benefits=feature['benefits'])
