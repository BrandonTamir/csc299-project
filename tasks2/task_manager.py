import json
import os

# Define the file where tasks will be stored
TASKS_FILE = "tasks.json"

def load_tasks():
    """Loads tasks from the tasks.json file."""
    # Check if the file exists
    if not os.path.exists(TASKS_FILE):
        return []  # Return an empty list if no file
    
    # Open the file and load the JSON data
    try:
        with open(TASKS_FILE, 'r') as f:
            tasks = json.load(f)
            return tasks
    except json.JSONDecodeError:
        return [] # Return empty list if file is empty or corrupted

def save_tasks(tasks):
    """Saves the current list of tasks to the tasks.json file."""
    # Open the file in 'write' mode and dump the data
    with open(TASKS_FILE, 'w') as f:
        # indent=4 makes the JSON file human-readable
        json.dump(tasks, f, indent=4)

def view_tasks(tasks):
    """Displays the list of tasks."""
    if not tasks:
        print("\nYour to-do list is empty.")
        return

    print("\n--- Your To-Do List ---")
    # Enumerate to get an index (starting from 1)
    for i, task in enumerate(tasks):
        # Check the status and create a marker
        status_marker = "✓" if task['status'] == 'completed' else " "
        print(f"  [{status_marker}] {i + 1}. {task['description']}")
    print("-------------------------")

def add_task(tasks):
    """Adds a new task to the list."""
    description = input("Enter the task description: ")
    
    # A task is now a dictionary, not just a string
    task = {
        "description": description,
        "status": "pending"  # New feature: status
    }
    tasks.append(task)
    save_tasks(tasks) # Save after adding
    print(f"Added task: '{description}'")

def complete_task(tasks):
    """Marks a task as completed."""
    view_tasks(tasks)
    if not tasks:
        return # No tasks to complete

    try:
        task_num_str = input("Enter the task number to mark as complete: ")
        task_num = int(task_num_str)

        if 0 < task_num <= len(tasks):
            # Adjust for 0-based index
            task_index = task_num - 1
            
            # Update the status
            if tasks[task_index]['status'] == 'completed':
                print("That task is already marked as complete.")
            else:
                tasks[task_index]['status'] = 'completed'
                save_tasks(tasks) # Save after updating
                print(f"Marked task {task_num} as complete.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def main_menu():
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

# Run the main menu when the script is executed
if __name__ == "__main__":
    main_menu()