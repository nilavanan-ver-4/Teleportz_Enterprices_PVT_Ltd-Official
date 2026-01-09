import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# --- Configuration ---
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-this-in-prod'
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'database', 'site.db')
    SESSION_COOKIE_NAME = 'teleportz_official_session'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

# --- Extensions ---
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'admin.login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    # Try loading as regular admin User first
    user = db.session.get(User, int(user_id))
    if user:
        return user
    # Try loading as MarketingUser
    m_user = db.session.get(MarketingUser, int(user_id))
    if m_user:
        return m_user
    # Finally try loading as FinanceUser
    return db.session.get(FinanceUser, int(user_id))

# --- Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class CareerUser(UserMixin, db.Model):
    __tablename__ = 'career_user'
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    otp = db.Column(db.String(6))
    otp_expiry = db.Column(db.DateTime)
    is_verified = db.Column(db.Boolean, default=False)
    full_name = db.Column(db.String(200))
    email = db.Column(db.String(200))
    experience_summary = db.Column(db.Text)
    education = db.Column(db.Text)
    skills = db.Column(db.Text)
    resume_path = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Inquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    received_at = db.Column(db.DateTime, default=datetime.utcnow)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    experience = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    benefits = db.Column(db.Text, nullable=True)
    salary_range = db.Column(db.String(50), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    applications = db.relationship('JobApplication', backref='job', lazy=True, cascade='all, delete-orphan')

class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('career_user.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)
    cover_letter = db.Column(db.Text, nullable=True)
    resume_filename = db.Column(db.String(100), nullable=True)
    photo_filename = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default='pending')
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

class ApplicationTracking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('job_application.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text)
    update_time = db.Column(db.DateTime, default=datetime.utcnow)
    application = db.relationship('JobApplication', backref=db.backref('tracking_records', lazy=True, order_by='ApplicationTracking.update_time.desc()'))

class MarketingUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='marketer')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class BotConnectionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(50), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='success')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.Column(db.Text)

class SocialConnection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(50), nullable=False)
    account_name = db.Column(db.String(100))
    status = db.Column(db.String(20), default='inactive') # linked, inactive, pending
    auth_token = db.Column(db.String(255))
    last_sync = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('marketing_user.id'))

# --- Finance Management Models ---
class FinanceUser(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='accountant') # CFO, manager, accountant

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class FinancialAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(50), nullable=False) # Cash, Bank, AR, AP, Asset, Liability
    currency = db.Column(db.String(10), default='USD')
    balance = db.Column(db.Float, default=0.0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

class TradeInvoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    invoice_type = db.Column(db.String(20)) # Import, Export
    client_name = db.Column(db.String(150), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='USD')
    status = db.Column(db.String(20), default='unpaid') # paid, unpaid, partially_paid, overdue
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FinancialTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('financial_account.id'))
    invoice_id = db.Column(db.Integer, db.ForeignKey('trade_invoice.id'), nullable=True)
    transaction_type = db.Column(db.String(20)) # Credit, Debit
    category = db.Column(db.String(50)) # Freight, Customs, Sale, Purchase, Salary
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='USD')
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    performed_by = db.Column(db.Integer, db.ForeignKey('finance_user.id'))
    author = db.relationship('FinanceUser', backref='transactions')

class BudgetPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(50), nullable=False)
    period_year = db.Column(db.Integer, nullable=False)
    period_month = db.Column(db.Integer)
    allocated_amount = db.Column(db.Float, nullable=False)
    spent_amount = db.Column(db.Float, default=0.0)
    currency = db.Column(db.String(10), default='USD')

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    department = db.Column(db.String(100))
    monthly_salary = db.Column(db.Float, nullable=False)
    joining_date = db.Column(db.DateTime, default=datetime.utcnow)
    bank_details = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)

class SalaryPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    month_period = db.Column(db.String(20)) # e.g., "January 2026"
    status = db.Column(db.String(20), default='Processed')
    transaction_ref = db.Column(db.String(100))

class FundAllocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(150), nullable=False)
    allocated_amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50)) # R&D, Marketing, Shipping, Customs
    status = db.Column(db.String(20), default='Active')
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    performed_by = db.Column(db.Integer, db.ForeignKey('finance_user.id'))

class FinancialReminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime, nullable=False)
    priority = db.Column(db.String(20), default='Medium') # High, Medium, Low
    is_completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('finance_user.id'))

# --- Application Factory ---
def create_app(config_class=Config, register_blueprints=True):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    # Configure Logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')

    if register_blueprints:
        from admin.routes import admin_bp
        from official.routes import official_bp
        from botConnections.routes import bot_bp
        from financeTeleportz.routes import finance_bp

        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(official_bp)
        app.register_blueprint(bot_bp, url_prefix='/marketing')
        app.register_blueprint(finance_bp, url_prefix='/finance')

    # Ensure upload folders exist
    with app.app_context():
        upload_path = os.path.join(app.instance_path, 'uploads')
        resumes_path = os.path.join(app.instance_path, 'uploads', 'resumes')
        photos_path = os.path.join(app.instance_path, 'uploads', 'photos')
        os.makedirs(upload_path, exist_ok=True)
        os.makedirs(resumes_path, exist_ok=True)
        os.makedirs(photos_path, exist_ok=True)

    return app
