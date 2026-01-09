from app import create_app, db
import os

def fix_database():
    app = create_app()
    with app.app_context():
        print("Dropping existing finance tables to update schema...")
        # Since SQLite doesn't support easy ALTER TABLE for foreign keys, 
        # and this is a dev environment, we drop and recreate.
        
        # Core finance tables to refresh
        tables_to_refresh = [
            'financial_transaction', 
            'fund_allocation', 
            'financial_reminder', 
            'trade_invoice', 
            'budget_plan',
            'employee',
            'salary_payment'
        ]
        
        # We'll use raw SQL to drop them safely in SQLite
        for table in tables_to_refresh:
            try:
                db.session.execute(db.text(f"DROP TABLE IF EXISTS {table}"))
                print(f"Dropped {table}")
            except Exception as e:
                print(f"Error dropping {table}: {e}")
        
        db.session.commit()
        
        print("Recreating database tables with new schema (performed_by, etc)...")
        db.create_all()
        print("Database schema updated successfully.")

if __name__ == '__main__':
    fix_database()
