from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db, FinanceUser, FinancialAccount, FinancialTransaction, TradeInvoice, BudgetPlan, Employee, SalaryPayment, FundAllocation, FinancialReminder
from datetime import datetime, timedelta
import uuid

finance_bp = Blueprint('finance', __name__, template_folder='templates', static_folder='static')

@finance_bp.route('/')
@login_required
def dashboard():
    # Filtering Logic
    period = request.args.get('period', 'all')
    now = datetime.utcnow()
    query = FinancialTransaction.query
    
    if period == 'today':
        query = query.filter(FinancialTransaction.timestamp >= now.replace(hour=0, minute=0, second=0))
    elif period == 'week':
        query = query.filter(FinancialTransaction.timestamp >= now - timedelta(days=7))
    elif period == 'month':
        query = query.filter(FinancialTransaction.timestamp >= now - timedelta(days=30))
        
    transactions = query.order_by(FinancialTransaction.timestamp.desc()).limit(20).all()
    accounts = FinancialAccount.query.all()
    invoices = TradeInvoice.query.order_by(TradeInvoice.created_at.desc()).limit(15).all()
    budgets = BudgetPlan.query.filter_by(period_year=now.year).all()
    employees = Employee.query.all()
    funds = FundAllocation.query.all()
    
    # Reminders & Alerts
    reminders = FinancialReminder.query.filter_by(is_completed=False).order_by(FinancialReminder.due_date.asc()).all()
    
    # Dynamic Totals
    total_balance = sum(acc.balance for acc in accounts if acc.account_type in ['Cash', 'Bank'])
    ar_total = sum(inv.total_amount for inv in invoices if inv.status != 'paid')
    total_payroll = sum(e.monthly_salary for e in employees if e.is_active)
    
    return render_template('financeTeleportz/dashboard.html', 
                           accounts=accounts, 
                           transactions=transactions,
                           invoices=invoices,
                           budgets=budgets,
                           employees=employees,
                           funds=funds,
                           reminders=reminders,
                           total_balance=total_balance,
                           ar_total=ar_total,
                           total_payroll=total_payroll,
                           current_period=period)

@finance_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('finance.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = FinanceUser.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('finance.dashboard'))
        else:
            flash('Invalid credentials', 'danger')
            
    return render_template('financeTeleportz/login.html')

@finance_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('finance.login'))

@finance_bp.route('/action/add-transaction', methods=['POST'])
@login_required
def add_transaction():
    data = request.form
    account = FinancialAccount.query.filter_by(id=data.get('account_id')).first()
    if not account:
        flash("Account not found", "danger")
        return redirect(url_for('finance.dashboard'))
    
    amount = float(data.get('amount'))
    tx_type = data.get('type')
    
    if tx_type == 'Debit':
        account.balance -= amount
    else:
        account.balance += amount
        
    new_tx = FinancialTransaction(
        account_id=account.id,
        transaction_type=tx_type,
        category=data.get('category'),
        amount=amount,
        description=data.get('description'),
        performed_by=current_user.id
    )
    db.session.add(new_tx)
    db.session.commit()
    flash(f"Recorded by {current_user.username}", "success")
    return redirect(url_for('finance.dashboard'))

@finance_bp.route('/action/process-salary', methods=['POST'])
@login_required
def process_salary():
    emp_id = request.form.get('employee_id')
    emp = Employee.query.get(emp_id)
    account = FinancialAccount.query.filter_by(account_type='Bank').first()
    
    if emp and account and account.balance >= emp.monthly_salary:
        account.balance -= emp.monthly_salary
        payment = SalaryPayment(
            employee_id=emp.id,
            amount_paid=emp.monthly_salary,
            month_period=datetime.utcnow().strftime("%B %Y"),
            transaction_ref=str(uuid.uuid4())[:8].upper()
        )
        tx = FinancialTransaction(
            account_id=account.id,
            transaction_type='Debit',
            category='Payroll',
            amount=emp.monthly_salary,
            description=f"Salary for {emp.full_name}",
            performed_by=current_user.id
        )
        db.session.add(payment)
        db.session.add(tx)
        db.session.commit()
        flash(f"Payroll processed by {current_user.username}", "success")
    else:
        flash("Insufficient funds", "danger")
        
    return redirect(url_for('finance.dashboard'))

@finance_bp.route('/action/add-reminder', methods=['POST'])
@login_required
def add_reminder():
    title = request.form.get('title')
    due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%dT%H:%M')
    priority = request.form.get('priority')
    
    reminder = FinancialReminder(
        title=title,
        due_date=due_date,
        priority=priority,
        user_id=current_user.id
    )
    db.session.add(reminder)
    db.session.commit()
    flash("Reminder synchronized with global calendar.", "info")
    return redirect(url_for('finance.dashboard'))

@finance_bp.route('/action/clear-data', methods=['POST'])
@login_required
def clear_data():
    if current_user.role != 'CFO':
        flash("Admin Clearance Required", "danger")
        return redirect(url_for('finance.dashboard'))
        
    FinancialTransaction.query.delete()
    TradeInvoice.query.delete()
    BudgetPlan.query.delete()
    Employee.query.delete()
    SalaryPayment.query.delete()
    FundAllocation.query.delete()
    FinancialReminder.query.delete()
    
    accounts = FinancialAccount.query.all()
    for acc in accounts: acc.balance = 0.0
        
    db.session.commit()
    flash(f"System wiped by CFO {current_user.username}", "info")
    return redirect(url_for('finance.dashboard'))
