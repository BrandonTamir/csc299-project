# Task Manager (Python CLI)

Small class-project CLI to manage tasks stored in `tasks.json`.

Quick start (PowerShell)

1. Run the CLI (no venv):

```powershell
python tasks.py add "Finish homework"
python tasks.py list
python tasks.py complete 1
python tasks.py delete 1
```

2. If you use the repository virtual environment created earlier, run Python from the venv. Example (the environment configured in this workspace):

```powershell
C:/Users/brand/temp-tasks-build/.venv/Scripts/python.exe tasks.py add "Finish homework"
```

Running tests

From the repo root run (PowerShell):

```powershell
# Uses unittest discovery
python -m unittest tests.test_tasks
```

Notes

- Tasks are stored in `tasks.json` in the repository root.
- The CLI supports `add <description>`, `list`, `complete <id>`, and `delete <id>`.
- Writes are atomic (temporary file + replace). If `tasks.json` is missing it will be created.
