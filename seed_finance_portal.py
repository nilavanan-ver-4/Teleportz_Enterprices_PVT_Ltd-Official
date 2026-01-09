from app import create_app, db, FinanceUser, FinancialAccount, TradeInvoice, FinancialTransaction, BudgetPlan
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def seed_finance_data():
    app = create_app()
    with app.app_context():
        db.create_all()
        
        # 1. Create Finance User
        user = FinanceUser.query.filter_by(username='finance_admin').first()
        if not user:
            new_user = FinanceUser(
                username='finance_admin',
                email='finance@teleportz.com',
                role='CFO'
            )
            new_user.set_password('teleportz_fin_2026')
            db.session.add(new_user)
            print("Finance admin created: finance_admin / teleportz_fin_2026")

        # 2. Create Accounts
        if not FinancialAccount.query.first():
            main_bank = FinancialAccount(account_name='Standard Chartered - USD', account_type='Bank', currency='USD', balance=1250000.00)
            opex_cash = FinancialAccount(account_name='OPEX Cash Reserve', account_type='Cash', currency='USD', balance=75000.00)
            db.session.add_all([main_bank, opex_cash])
            db.session.flush()

            # 3. Create Demo Invoices
            inv1 = TradeInvoice(
                invoice_number='INV-2026-001',
                invoice_type='Export',
                client_name='Global Tech Logistics',
                total_amount=245000.00,
                status='unpaid',
                due_date=datetime.utcnow() + timedelta(days=15)
            )
            inv2 = TradeInvoice(
                invoice_number='IMP-2026-042',
                invoice_type='Import',
                client_name='Shenzhen Port Authorities',
                total_amount=12400.00,
                status='paid',
                due_date=datetime.utcnow() - timedelta(days=2)
            )
            db.session.add_all([inv1, inv2])
            db.session.flush()

            # 4. Create Transactions
            tx1 = FinancialTransaction(
                account_id=opex_cash.id,
                transaction_type='Debit',
                category='Customs',
                amount=12400.00,
                description='Shenzhen import duty settlement'
            )
            tx2 = FinancialTransaction(
                account_id=main_bank.id,
                transaction_type='Credit',
                category='Trade Sale',
                amount=85000.00,
                description='Partial payment for Tech Order #88'
            )
            db.session.add_all([tx1, tx2])

            # 5. Create budgets
            b1 = BudgetPlan(department='Logistics', period_year=2026, allocated_amount=500000.00, spent_amount=125000.00)
            b2 = BudgetPlan(department='Operations', period_year=2026, allocated_amount=200000.00, spent_amount=45000.00)
            db.session.add_all([b1, b2])

        db.session.commit()
        print("Finance demo data seeded successfully.")

if __name__ == '__main__':
    seed_finance_data()
