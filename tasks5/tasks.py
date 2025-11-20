#!/usr/bin/env python3
"""Simple CLI Task Manager

Usage: python tasks.py <command> [args]

Commands:
  add <description>
  list
  complete <id>
  delete <id>

Stores tasks in tasks.json at the repository root.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime
from typing import List, Dict, Any

TASKS_FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


def load_tasks() -> List[Dict[str, Any]]:
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            print(f"Error: {TASKS_FILE} does not contain a JSON array.", file=sys.stderr)
            sys.exit(4)
        return data
    except json.JSONDecodeError:
        print(f"Error: {TASKS_FILE} contains invalid JSON. Fix or remove the file.", file=sys.stderr)
        sys.exit(4)
    except OSError as e:
        print(f"Error reading {TASKS_FILE}: {e}", file=sys.stderr)
        sys.exit(4)


def save_tasks(tasks: List[Dict[str, Any]]) -> None:
    # atomic write: write to temp file then replace
    dirpath = os.path.dirname(TASKS_FILE) or "."
    fd, tmp_path = tempfile.mkstemp(prefix="tasks.json.", dir=dirpath)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as tmpf:
            json.dump(tasks, tmpf, indent=2, ensure_ascii=False)
            tmpf.flush()
            os.fsync(tmpf.fileno())
        os.replace(tmp_path, TASKS_FILE)
    except OSError as e:
        print(f"Error writing {TASKS_FILE}: {e}", file=sys.stderr)
        # best-effort cleanup
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass
        sys.exit(4)


def next_id(tasks: List[Dict[str, Any]]) -> int:
    if not tasks:
        return 1
    try:
        return max(int(t.get("id", 0)) for t in tasks) + 1
    except Exception:
        # fallback
        return len(tasks) + 1


def add_task(description: str) -> Dict[str, Any]:
    desc = description.strip()
    if not desc:
        print("Error: description cannot be empty.", file=sys.stderr)
        sys.exit(2)
    tasks = load_tasks()
    tid = next_id(tasks)
    task = {
        "id": tid,
        "description": desc,
        "completed": False,
        "created_at": datetime.utcnow().isoformat() + "Z",
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task {tid}: {desc}")
    return task


def list_tasks() -> None:
    tasks = load_tasks()
    incomplete = [t for t in tasks if not t.get("completed")]
    if not incomplete:
        print("No incomplete tasks.")
        return
    for t in incomplete:
        print(f"{t.get('id')}. {t.get('description')}")


def find_task(tasks: List[Dict[str, Any]], tid: int) -> Dict[str, Any] | None:
    for t in tasks:
        try:
            if int(t.get("id")) == tid:
                return t
        except Exception:
            continue
    return None


def complete_task(tid: int) -> None:
    tasks = load_tasks()
    task = find_task(tasks, tid)
    if task is None:
        print(f"Error: task {tid} not found.", file=sys.stderr)
        sys.exit(3)
    task["completed"] = True
    save_tasks(tasks)
    print(f"Task {tid} marked completed.")


def delete_task(tid: int) -> None:
    tasks = load_tasks()
    task = find_task(tasks, tid)
    if task is None:
        print(f"Error: task {tid} not found.", file=sys.stderr)
        sys.exit(3)
    tasks = [t for t in tasks if not (int(t.get("id", -1)) == tid)]
    save_tasks(tasks)
    print(f"Task {tid} deleted.")


def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="tasks.py", description="Simple CLI Task Manager")
    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add", help="Add a new task")
    p_add.add_argument("description", nargs="+", help="Task description")

    sub.add_parser("list", help="List incomplete tasks")

    p_complete = sub.add_parser("complete", help="Mark task completed")
    p_complete.add_argument("id", help="Task id to mark complete")

    p_delete = sub.add_parser("delete", help="Delete a task")
    p_delete.add_argument("id", help="Task id to delete")

    return parser.parse_args(argv)


def main(argv: List[str]) -> None:
    args = parse_args(argv)
    cmd = args.command
    if cmd == "add":
        description = " ".join(args.description)
        add_task(description)
    elif cmd == "list":
        list_tasks()
    elif cmd == "complete":
        try:
            tid = int(args.id)
        except ValueError:
            print("Error: id must be an integer.", file=sys.stderr)
            sys.exit(2)
        complete_task(tid)
    elif cmd == "delete":
        try:
            tid = int(args.id)
        except ValueError:
            print("Error: id must be an integer.", file=sys.stderr)
            sys.exit(2)
        delete_task(tid)
    else:
        print("No command provided. Use add/list/complete/delete.")
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
