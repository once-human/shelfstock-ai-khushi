import sqlite3
import json
from pathlib import Path

DB_FILE = "data/app_data.db"
SUPPLIERS_JSON = Path("data/suppliers.json")
WORKERS_JSON = Path("data/workers.json")

def init_database():
    """Creates the SQLite database and tables if they don't exist."""
    db_path = Path(DB_FILE)
    db_path.parent.mkdir(exist_ok=True)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create Suppliers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS suppliers (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        rating REAL,
        specialties TEXT, -- Storing list as JSON string
        contact_email TEXT
    )
    """)
    
    # Create Workers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workers (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT,
        availability INTEGER, -- 0 for False, 1 for True
        current_tasks INTEGER
    )
    """)
    
    # --- Data Migration (Optional - Run once) ---
    # Check if suppliers table is empty before migrating
    cursor.execute("SELECT COUNT(*) FROM suppliers")
    if cursor.fetchone()[0] == 0 and SUPPLIERS_JSON.exists():
        print(f"Migrating data from {SUPPLIERS_JSON}...")
        try:
            with open(SUPPLIERS_JSON, 'r') as f:
                data = json.load(f)
                suppliers_data = data.get('suppliers', [])
                for s in suppliers_data:
                    cursor.execute("""
                    INSERT INTO suppliers (id, name, rating, specialties, contact_email)
                    VALUES (?, ?, ?, ?, ?)
                    """, (
                        s.get('id'), 
                        s.get('name'), 
                        s.get('rating'), 
                        json.dumps(s.get('specialties', [])), # Store list as JSON string
                        s.get('contact_email')
                    ))
            print("Supplier data migrated.")
        except Exception as e:
            print(f"Error migrating supplier data: {e}")
            
    # Check if workers table is empty before migrating
    cursor.execute("SELECT COUNT(*) FROM workers")
    if cursor.fetchone()[0] == 0 and WORKERS_JSON.exists():
        print(f"Migrating data from {WORKERS_JSON}...")
        try:
            with open(WORKERS_JSON, 'r') as f:
                data = json.load(f)
                workers_data = data.get('workers', [])
                for w in workers_data:
                    cursor.execute("""
                    INSERT INTO workers (id, name, role, availability, current_tasks)
                    VALUES (?, ?, ?, ?, ?)
                    """, (
                        w.get('id'), 
                        w.get('name'), 
                        w.get('role'), 
                        1 if w.get('availability', False) else 0, # Convert bool to int
                        w.get('current_tasks')
                    ))
            print("Worker data migrated.")
        except Exception as e:
            print(f"Error migrating worker data: {e}")
            
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_database()
    # You can now optionally delete the source JSON files if migration was successful
    # try:
    #     SUPPLIERS_JSON.unlink()
    #     WORKERS_JSON.unlink()
    #     print("Source JSON files deleted.")
    # except OSError as e:
    #     print(f"Error deleting JSON files: {e}") 