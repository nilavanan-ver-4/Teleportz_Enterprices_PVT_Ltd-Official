import sqlite3
import os

db_path = r'e:\Teleportz_Enterprices_PVT_Ltd-Official\database\site.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    tables_to_drop = ['career_user', 'job_application', 'application_tracking', 'job']
    for table in tables_to_drop:
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            print(f"Dropped {table}")
        except Exception as e:
            print(f"Error dropping {table}: {e}")
            
    conn.commit()
    conn.close()
    print("Database cleanup completed.")
else:
    print("Database not found.")
