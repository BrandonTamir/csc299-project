# tasks3/src/__init__.py

# --- Part 1: Example Function ---
def inc(n: int) -> int:
    return n + 1

# --- Part 2: Your Task Manager Code ---
# (Copy all your imports from tasks2 here)
import json
import os

# (Copy all your helper functions from tasks2 here)
# TASKS_FILE, load_tasks, save_tasks, view_tasks, etc.
TASKS_FILE = "tasks.json"

def load_tasks():
    """Loads tasks from the tasks.json file."""
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r') as f:
            tasks = json.load(f)
            return tasks
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    """Saves the current list of tasks to the tasks.json file."""
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

def view_tasks(tasks):
    """Displays the list of tasks."""
    if not tasks:
        print("\nYour to-do list is empty.")
        return
    print("\n--- Your To-Do List ---")
    for i, task in enumerate(tasks):
        status_marker = "✓" if task['status'] == 'completed' else " "
        print(f"  [{status_marker}] {i + 1}. {task['description']}")
    print("-------------------------")

def add_task(tasks):
    """Adds a new task to the list."""
    description = input("Enter the task description: ")
    task = {
        "description": description,
        "status": "pending"
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task: '{description}'")

def complete_task(tasks):
    """Marks a task as completed."""
    view_tasks(tasks)
    if not tasks:
        return
    try:
        task_num_str = input("Enter the task number to mark as complete: ")
        task_num = int(task_num_str)
        if 0 < task_num <= len(tasks):
            task_index = task_num - 1
            if tasks[task_index]['status'] == 'completed':
                print("That task is already marked as complete.")
            else:
                tasks[task_index]['status'] = 'completed'
                save_tasks(tasks)
                print(f"Marked task {task_num} as complete.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

# -----------------------------------------------------------------
# CRITICAL CHANGE: Rename 'main_menu' to 'main'
# 'uv run tasks3' will call this function automatically.
# -----------------------------------------------------------------
def main():
    """Displays the main menu and handles user input."""
    tasks = load_tasks() # Load tasks at the start

    while True:
        print("\n===== To-Do List Manager =====")
        print("1. View all tasks")
        print("2. Add a new task")
        print("3. Mark a task as complete")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            complete_task(tasks)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

# Note: You do NOT need the 'if __name__ == "__main__":' block anymore.