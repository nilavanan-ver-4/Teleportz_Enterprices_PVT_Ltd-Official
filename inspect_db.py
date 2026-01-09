import sqlite3
import os

db_path = r'e:\Teleportz_Enterprices_PVT_Ltd-Official\database\site.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in site.db:")
    for table in tables:
        print(f"- {table[0]}")
        cursor.execute(f"PRAGMA table_info({table[0]})")
        columns = cursor.fetchall()
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
    conn.close()
else:
    print("Database not found.")
