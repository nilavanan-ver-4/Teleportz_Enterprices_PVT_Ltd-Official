from app import create_app, db, FinanceUser, FinancialAccount, Employee
from werkzeug.security import generate_password_hash

def seed_finance_dynamic():
    app = create_app()
    with app.app_context():
        # Clear existing models related to the old data
        db.create_all()
        
        # 1. Ensure Finance CFO exists
        user = FinanceUser.query.filter_by(username='finance_admin').first()
        if not user:
            new_user = FinanceUser(
                username='finance_admin',
                email='finance@teleportz.com',
                role='CFO'
            )
            new_user.set_password('teleportz_fin_2026')
            db.session.add(new_user)
        
        # 2. Add Base Accounts if empty
        if not FinancialAccount.query.first():
            bank = FinancialAccount(account_name='Trading Bank Hub', account_type='Bank', currency='USD', balance=500000.00)
            cash = FinancialAccount(account_name='Local Cash Vault', account_type='Cash', currency='USD', balance=15000.00)
            db.session.add_all([bank, cash])
            
        # 3. Add initial Employees for Salary Handling
        if not Employee.query.first():
            db.session.add_all([
                Employee(full_name='Nilavanan Raj', employee_id='EMP001', department='Logistics', monthly_salary=8500.00),
                Employee(full_name='Sarah Chen', employee_id='EMP002', department='Trade Compliance', monthly_salary=7200.00),
                Employee(full_name='Marcus Thorne', employee_id='EMP003', department='Market Operations', monthly_salary=6800.00)
            ])
            
        db.session.commit()
        print("Dynamic Finance environment initialized.")

if __name__ == '__main__':
    seed_finance_dynamic()
