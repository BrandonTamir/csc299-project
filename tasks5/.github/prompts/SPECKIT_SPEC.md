# SPECKIT SPEC: Python CLI Task Manager

Overview
--------
This document specifies a simple Python command-line Task Manager intended for a class project. It describes language, storage, features, command usage, data format, edge cases, and minimal testing guidance.

Language
--------
- Python (3.8+ recommended).

Storage
-------
- All tasks are persisted to a local file named `tasks.json` at the project root.
- The file contains a JSON array of task objects. The CLI reads and writes this file for all operations.

Task object schema
------------------
- A task is a JSON object with these fields:
  - id: integer (unique, sequential or monotonic)
  - description: string
  - completed: boolean
  - created_at: string (ISO 8601 timestamp)

Example `tasks.json` (initial):

[]

Example `tasks.json` (after two adds):

[
  {"id": 1, "description": "Write lab report", "completed": false, "created_at": "2025-11-19T12:00:00Z"},
  {"id": 2, "description": "Study for quiz", "completed": false, "created_at": "2025-11-19T12:05:00Z"}
]

CLI features & usage
---------------------
The CLI exposes the following commands and behaviors.

1) add <description>
   - Usage (PowerShell):
     python tasks.py add "Finish homework"
   - Action: Create a new task with the provided description, assign a unique integer `id`, set `completed` to `false`, set `created_at` to now (ISO 8601), and append the task to `tasks.json`.
   - Output: Print the created task's `id` and description. Exit code 0 on success.

2) list
   - Usage:
     python tasks.py list
   - Action: Read `tasks.json` and print all incomplete tasks (where `completed` is false), one per line, formatted as: `ID. description`.
   - Output example:
     1. Write lab report
     2. Study for quiz
   - Exit code 0 on success. If no incomplete tasks, print a friendly message (e.g., "No incomplete tasks.").

3) complete <id>
   - Usage:
     python tasks.py complete 2
   - Action: Mark the task with the given integer `id` as `completed = true` in `tasks.json`.
   - Output: On success, print a confirmation (e.g., "Task 2 marked completed."). If `id` not found, print an error and exit with non-zero status.

4) delete <id>
   - Usage:
     python tasks.py delete 3
   - Action: Remove the task with the given `id` from `tasks.json`.
   - Output: On success, print a confirmation (e.g., "Task 3 deleted."). If `id` not found, print an error and exit non-zero.

Operational details
-------------------
- File I/O: Use read-modify-write with an atomic replace: write to a temporary file (e.g., `tasks.json.tmp`) and rename over `tasks.json` to avoid partial writes.
- ID generation: Use the max existing `id` + 1. If file empty, start at 1.
- Concurrency: This spec expects single-user usage. If concurrent runs are a concern, add OS-level file locking or discourage concurrent execution in README.
- Validation: Trim description whitespace and reject empty descriptions with an error message.

Errors & exit codes
-------------------
- Exit code 0: success.
- Exit code 2: invalid usage or missing required argument.
- Exit code 3: task `id` not found.
- Exit code 4: I/O error (unable to read/write `tasks.json`).

Edge cases
----------
- If `tasks.json` is missing, the CLI should create it with an empty array before performing the operation.
- If `tasks.json` contains invalid JSON, print an error suggesting to fix or delete the file and exit non-zero.
- If `complete` or `delete` is called with a non-integer `id`, print a usage error (exit code 2).

Examples (end-to-end)
---------------------
- Add a task:
  - Command: `python tasks.py add "Finish homework"`
  - Output: `Added task 1: Finish homework`

- List incomplete tasks:
  - Command: `python tasks.py list`
  - Output:
    1. Finish homework

- Mark complete:
  - Command: `python tasks.py complete 1`
  - Output: `Task 1 marked completed.`

- Delete a task:
  - Command: `python tasks.py delete 1`
  - Output: `Task 1 deleted.`

Minimal implementation notes (for developer)
------------------------------------------
- Single source file `tasks.py` with a small CLI parser (argparse or click). Argparse is acceptable and has no extra deps.
- Helper functions:
  - load_tasks() -> list[dict]
  - save_tasks(list[dict])
  - next_id(tasks) -> int
  - add_task(description)
  - list_tasks()
  - complete_task(id)
  - delete_task(id)
- Use `datetime.datetime.utcnow().isoformat() + 'Z'` for `created_at`.

Testing
-------
- Unit tests should cover the helpers (load/save/next_id/add/complete/delete) and edge cases (missing file, invalid JSON, non-existent id).
- Integration: a small script test that runs the CLI commands in sequence against a temporary directory and asserts the `tasks.json` content.

Notes
-----
- This spec is intentionally minimal to fit a class project. Extensions (priorities, due dates, persistence backends, interactive TUI) are out of scope for the initial deliverable.

---
Requested: a spec for a Python CLI Task Manager that uses `tasks.json` and supports `add`, `list`, `complete`, and `delete` commands.
