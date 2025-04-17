import sqlite3
import json
from pathlib import Path
import streamlit as st # Import streamlit for error display

DB_FILE = Path("data/app_data.db")

def _get_db_connection():
    """Establishes a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row # Return rows as dictionary-like objects
        return conn
    except sqlite3.Error as e:
        st.error(f"Database connection error: {e}")
        return None

def load_suppliers():
    """Load all suppliers from the database."""
    conn = _get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, rating, specialties, contact_email FROM suppliers ORDER BY name")
        suppliers = [dict(row) for row in cursor.fetchall()]
        # Convert specialties back from JSON string to list
        for s in suppliers:
            try:
                s['specialties'] = json.loads(s.get('specialties', '[]'))
            except json.JSONDecodeError:
                s['specialties'] = [] # Default to empty list if JSON is invalid
        conn.close()
        return suppliers
    except sqlite3.Error as e:
        st.error(f"Error loading suppliers from database: {e}")
        if conn: conn.close()
        return []

def load_workers():
    """Load all workers from the database."""
    conn = _get_db_connection()
    if not conn:
        return []
        
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, role, availability, current_tasks FROM workers ORDER BY name")
        workers = [dict(row) for row in cursor.fetchall()]
        # Convert availability back from int to bool
        for w in workers:
            w['availability'] = bool(w.get('availability', 0))
        conn.close()
        return workers
    except sqlite3.Error as e:
        st.error(f"Error loading workers from database: {e}")
        if conn: conn.close()
        return []

def get_available_workers():
    """Get list of workers who are available from the database."""
    conn = _get_db_connection()
    if not conn:
        return []
        
    try:
        cursor = conn.cursor()
        # Filter directly in the SQL query
        cursor.execute("SELECT id, name, role, availability, current_tasks FROM workers WHERE availability = 1 ORDER BY name")
        workers = [dict(row) for row in cursor.fetchall()]
        # Convert availability back from int to bool
        for w in workers:
            w['availability'] = True # We know they are available from the query
        conn.close()
        return workers
    except sqlite3.Error as e:
        st.error(f"Error loading available workers from database: {e}")
        if conn: conn.close()
        return []

def get_supplier_by_id(supplier_id):
    """Get a single supplier by their ID."""
    conn = _get_db_connection()
    if not conn or not supplier_id:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, rating, specialties, contact_email FROM suppliers WHERE id = ?", (supplier_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            supplier = dict(row)
            try:
                supplier['specialties'] = json.loads(supplier.get('specialties', '[]'))
            except json.JSONDecodeError:
                supplier['specialties'] = []
            return supplier
        else:
            return None
    except sqlite3.Error as e:
        st.error(f"Error fetching supplier {supplier_id}: {e}")
        if conn: conn.close()
        return None

def get_worker_by_id(worker_id):
    """Get a single worker by their ID."""
    conn = _get_db_connection()
    if not conn or not worker_id:
        return None
        
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, role, availability, current_tasks FROM workers WHERE id = ?", (worker_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            worker = dict(row)
            worker['availability'] = bool(worker.get('availability', 0))
            return worker
        else:
            return None
    except sqlite3.Error as e:
        st.error(f"Error fetching worker {worker_id}: {e}")
        if conn: conn.close()
        return None 