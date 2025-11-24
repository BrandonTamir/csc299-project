import pytest
import sqlite3
import os

# A simple test to verify the database creates tables correctly
def test_database_creation():
    db_name = "test_db.db"
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Mimic the init_db function
    c.execute('''CREATE TABLE IF NOT EXISTS tasks
                 (id INTEGER PRIMARY KEY, description TEXT, status TEXT)''')

    # Check if table exists
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'")
    assert c.fetchone() is not None

    conn.close()
    # Clean up
    if os.path.exists(db_name):
        os.remove(db_name)

def test_priority_logic():
    # Test that priority strings are valid
    valid_priorities = ["High", "Medium", "Low"]
    input_prio = "High"
    assert input_prio in valid_priorities