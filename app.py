import json
import sys

# The name of the file where tasks are stored
TASKS_FILE = "tasks.json"

def load_tasks():
    """Loads tasks from the JSON file."""
    try:
        # Open the file in read mode
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, return an empty list
        return []

def save_tasks(tasks):
    """Saves the list of tasks to the JSON file."""
    # Open the file in write mode
    with open(TASKS_FILE, 'w') as file:
        # Write the tasks list to the file, formatted nicely
        json.dump(tasks, file, indent=4)

def list_tasks():
    """Displays all tasks to the user."""
    tasks = load_tasks()
    if not tasks:
        print("No tasks found. Add one!")
    else:
        print("--- Your Tasks ---")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task['description']}")
    print("--------------------")

def add_task(description):
    """Adds a new task to the list."""
    tasks = load_tasks()
    # A task is a dictionary with a 'description' key
    new_task = {"description": description}
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"✅ Added task: '{description}'")
if __name__ == "__main__":
    # sys.argv is a list of words typed in the terminal
    # The first item (sys.argv[0]) is the script name, so we start at index 1
    if len(sys.argv) < 2:
        print("Usage: python app.py [list|add|search] [task description]")
        sys.exit(1) # Exit the script

    command = sys.argv[1]

    if command == "list":
        list_tasks()
    elif command == "add":
        # Combine the words of the task description
        task_description = " ".join(sys.argv[2:])
        if not task_description:
            print("❌ Error: Please provide a description for the task.")
        else:
            add_task(task_description)
    else:
        print(f"❌ Error: Unknown command '{command}'")
