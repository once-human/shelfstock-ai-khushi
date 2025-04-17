"""
data_save_helper.py

👋 About this file:
This module helps you save, retrieve, and manage structured data (like notes, tasks, messages)
in a local `.json` file—perfect for AI prototyping projects.

✨ Why use it?
Each time you run your prototype, this creates a new data file so your test session stays clean.
You can store your own Pydantic model objects here (things like user inputs, logs, ideas, etc.)

📚 Example:
You define a data model like `Note`, and use these functions to add, read, or update note entries.
"""

import json
import os
from datetime import datetime
from typing import List, Type, TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

# ---------- Global Config ----------

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
DATA_FILE = os.path.join(DATA_DIR, f"data_{TIMESTAMP}.json")


# ---------- File Initialization ----------

def init_data_store(initial_data: List[dict] = []) -> str:
    """
    Creates a new JSON file for this prototype session.

    Args:
        initial_data: Optional list of dicts to initialize the file with.

    Returns:
        Path to the newly created JSON file.

    Example:
        >>> init_data_store()
    """
    print("[init_data_store] Initializing data storage in json file...")
    with open(DATA_FILE, "w") as f:
        json.dump(initial_data, f, indent=4)
    print(f"[init_data_store] New data file created: {DATA_FILE}")
    return DATA_FILE


# ---------- CRUD Functions ----------

def read_data() -> List[dict]:
    """
    Loads all entries from the current data file.

    Returns:
        List of records as dictionaries.

    Example:
        >>> entries = read_data()
        >>> print(entries[0])
    """
    try:
        with open(DATA_FILE, "r") as f:
            response= json.load(f)
            print(f"[read_data]: {response}")
            return response
    except Exception as e:
        print(f"[load_data] Could not read data: {e}")
        return []


def save_data(entries: List[dict]) -> None:
    """
    Saves a list of records to the data file.

    Args:
        entries: List of dicts to save.

    Example:
        >>> save_data([{"id": 1, "text": "hello"}])
    """
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f, indent=4)
    print("[save_data] Data saved: " + entries)


def add_entry(entry: BaseModel) -> None:
    """
    Adds a new entry to the data file.

    Args:
        entry: A Pydantic model instance (e.g., your custom data object).

    Example:
        >>> note = Note(id="1", content="Test", tags="test")
        >>> add_entry(note)
    """
    data = read_data()
    data.append(entry.model_dump())
    save_data(data)
    print("[add_entry] Entry added.")


def update_entry(entry_id: str, updated_fields: dict) -> bool:
    """
    Updates an entry in the data file by its ID.

    Args:
        entry_id: The ID of the entry to update.
        updated_fields: Dict with fields to update.

    Returns:
        True if update succeeded, False if not found.

    Example:
        >>> update_entry("1", {"tags": "updated"})
    """
    data = read_data()
    found = False

    for item in data:
        if str(item.get("id")) == str(entry_id):
            item.update(updated_fields)
            found = True
            break

    if found:
        save_data(data)
        print(f"[update_entry] Entry {entry_id} updated.")
    else:
        print(f"[update_entry] Entry {entry_id} not found.")

    return found


def delete_entry(entry_id: str) -> bool:
    """
    Deletes an entry from the data file by its ID.

    Args:
        entry_id: The ID of the entry to delete.

    Returns:
        True if deleted, False if not found.

    Example:
        >>> delete_entry("1")
    """
    data = read_data()
    new_data = [item for item in data if str(item.get("id")) != str(entry_id)]

    if len(new_data) < len(data):
        save_data(new_data)
        print(f"[delete_entry] Entry {entry_id} deleted.")
        return True
    else:
        print(f"[delete_entry] Entry {entry_id} not found.")
        return False


def generate_unique_id() -> str:
    """
    Generates a new numeric ID based on existing entries.

    Returns:
        A string ID that is one higher than the current max.

    Example:
        >>> new_id = generate_unique_id()
    """
    data = read_data()
    existing_ids = []

    for item in data:
        try:
            existing_ids.append(int(item.get("id", 0)))
        except Exception:
            continue

    next_id = max(existing_ids, default=0) + 1
    return str(next_id)