# tasks3/tests/test_tasks.py

import pytest
from tasks3 import add_task, complete_task, load_tasks
import tasks3  # We need this to patch functions
import json
import os

# This 'fixture' runs before and after each test
@pytest.fixture(autouse=True)
def clean_up_tasks_file():
    """This fixture ensures tasks.json is deleted before/after each test."""
    # Code before 'yield' runs BEFORE the test
    if os.path.exists("tasks.json"):
        os.remove("tasks.json")
    
    yield  # This is where your test function runs
    
    # Code after 'yield' runs AFTER the test
    if os.path.exists("tasks.json"):
        os.remove("tasks.json")

# --- Test 1: Test the add_task function ---
def test_add_task(monkeypatch):
    """Verify that add_task adds a task to the list and saves it."""
    tasks = [] # Start with an empty list
    
    # Simulate the user typing "Buy groceries" and pressing Enter
    monkeypatch.setattr('builtins.input', lambda _: "Buy groceries")
    
    # Run the function
    add_task(tasks)
    
    # Check 1: Was the 'tasks' list in memory updated?
    assert len(tasks) == 1
    assert tasks[0]['description'] == "Buy groceries"
    assert tasks[0]['status'] == "pending"
    
    # Check 2: Was the 'tasks.json' file saved correctly?
    loaded_tasks = load_tasks() # Use our own function to read the file
    assert len(loaded_tasks) == 1
    assert loaded_tasks[0]['description'] == "Buy groceries"

# --- Test 2: Test the complete_task function ---
def test_complete_task(monkeypatch):
    """Verify that complete_task updates a task's status."""
    # Start with one pending task
    tasks = [{"description": "Write tests", "status": "pending"}]
    
    # Simulate the user typing "1" and pressing Enter
    monkeypatch.setattr('builtins.input', lambda _: "1")
    
    # We also 'patch' view_tasks so it doesn't print to the screen during tests
    monkeypatch.setattr(tasks3, 'view_tasks', lambda _: None)

    # Run the function
    complete_task(tasks)
    
    # Check 1: Was the 'tasks' list in memory updated?
    assert tasks[0]['status'] == "completed"
    
    # Check 2: Was the 'tasks.json' file saved correctly?
    loaded_tasks = load_tasks()
    assert loaded_tasks[0]['status'] == "completed"