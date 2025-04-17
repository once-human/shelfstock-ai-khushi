import json
from pathlib import Path

def load_suppliers():
    """Load supplier data from JSON file."""
    try:
        with open(Path('data/suppliers.json'), 'r') as f:
            data = json.load(f)
            return data.get('suppliers', [])
    except FileNotFoundError:
        return []

def load_workers():
    """Load worker data from JSON file."""
    try:
        with open(Path('data/workers.json'), 'r') as f:
            data = json.load(f)
            return data.get('workers', [])
    except FileNotFoundError:
        return []

def get_available_workers():
    """Get list of workers who are available."""
    workers = load_workers()
    return [w for w in workers if w.get('availability', False)] 