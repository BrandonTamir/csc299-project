# csc299-project
# Task Command-Line Application

This is a simple command-line application built with Python for managing a to-do list. It allows a user to add, list, and search for tasks, which are stored in a `tasks.json` data file.

This project was created for the CSC299 course.

## Requirements

* Python 3

## Setup Instructions

1.  Clone the repository to your local machine:
    ```bash
    git clone [https://github.com/](https://github.com/)[BrandonTamir]/csc299-project.git
    ```

2.  Navigate into the project directory:
    ```bash
    cd csc299-project/tasks1
    ```

## How to Use

The application is run from the command line using `python app.py` followed by a command.

### To Add a Task

Use the `add` command followed by the task description in quotes.

```bash
python app.py add "Submit the final project report"
```

### To List All Tasks

Use the `list` command to display all current tasks.

```bash
python app.py list
```

### To Search for a Task (Optional)

*(Note: If you haven't built the search function yet, you can either remove this section or leave it as a placeholder for what you plan to do.)*

Use the `search` command followed by a keyword to find matching tasks.

```bash
python app.py search "report"
```
