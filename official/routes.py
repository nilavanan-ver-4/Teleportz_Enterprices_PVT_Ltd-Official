from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import Product, Inquiry, db

official_bp = Blueprint('official', __name__, template_folder='templates', static_folder='static', static_url_path='/official/static')

@official_bp.route('/')
def home():
    products = Product.query.limit(3).all()
    return render_template('official/home.html', products=products)

@official_bp.route('/about')
def about():
    return render_template('official/about.html')

@official_bp.route('/services')
def services():
    return render_template('official/services.html')

@official_bp.route('/products')
def products():
    products = [
        {
            'name': 'RX-7 Massage Chair',
            'category': 'Premium Series',
            'description': 'World\'s Most Advanced Technology with futuristic capsule design. Features 7D full-body massage, SL track, AI body scan, zero gravity, and voice control.',
            'price': '₹2,05,000',
            'image_filename': ''
        },
        {
            'name': 'RX-5 Elite Massage Chair',
            'category': 'Elite Series',
            'description': 'Advanced 7D massage with automatic leg stretching, tri-motion calf rubbing, feet scraping, and full-body stretching for flexibility.',
            'price': '₹1,75,000',
            'image_filename': ''
        },
        {
            'name': 'Coin & QR-UPI Operated Chair',
            'category': 'Commercial Series',
            'description': 'Minimalist self-kiosk design engineered for commercial spaces (malls, airports). Supports Coin and QR-UPI payments. Heavy-duty build.',
            'price': '₹1,55,000',
            'image_filename': ''
        },
        {
            'name': 'RX-3 Massage Chair',
            'category': 'Advanced Series',
            'description': 'Features Dual SL Track system, tri-motion calf rubbing, and 7D full-body massage with zero gravity positioning.',
            'price': '₹1,45,000',
            'image_filename': ''
        },
        {
            'name': 'Q7 2.0 Massage Chair',
            'category': 'Smart Series',
            'description': 'Android-based touchscreen interface, TikTok/Reels controller, and mobile phone holder. Personalized 7D massage experience.',
            'price': '₹1,35,000',
            'image_filename': ''
        },
        {
            'name': 'R10 Massage Chair',
            'category': 'Luxury Series',
            'description': 'U-shaped head massage, navy blue leather, and extra cushioning. Intelligent AI body scan for personal home use.',
            'price': '₹99,000',
            'image_filename': ''
        },
         {
            'name': 'Q5 Massage Chair',
            'category': 'Wellness Series',
            'description': 'Exceptional 7D massage with SL track design. Features wireless phone charging and convenient voice control.',
            'price': '₹95,000',
            'image_filename': ''
        },
        {
            'name': 'R8 Pro Massage Chair',
            'category': 'Pro Series',
            'description': 'Upgraded faux leather with quick-access shortcut keys. 4D full-body massage and fixed roller system.',
            'price': '₹75,000',
            'image_filename': ''
        },
        {
            'name': 'R7 Neo Massage Chair',
            'category': 'Neo Series',
            'description': 'Sleek metal frame with 4D massage and fixed roller technology. Suitable for personal and commercial use (up to 150kg).',
            'price': '₹70,000',
            'image_filename': ''
        },
        {
            'name': 'R6 Massage Chair',
            'category': 'Classic Series',
            'description': 'Sturdy wooden frame with 4D massage system. Features therapeutic heating and targeted thigh massage.',
            'price': '₹55,000',
            'image_filename': ''
        }
    ]
    search = request.args.get('search', '') # Keep search for template, even if not used for filtering
    # No filtering logic here as products are hardcoded
    return render_template('official/products.html', products=products, search=search)

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
