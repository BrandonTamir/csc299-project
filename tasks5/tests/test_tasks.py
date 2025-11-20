import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

# Ensure repo root is on sys.path so `import tasks` works when running tests
repo_root = str(Path(__file__).resolve().parents[1])
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

import tasks


class TestTasksCLI(unittest.TestCase):
    def setUp(self) -> None:
        # create a temporary directory and point TASKS_FILE there
        self.tmpdir = tempfile.TemporaryDirectory()
        self.tasks_file = os.path.join(self.tmpdir.name, "tasks.json")
        tasks.TASKS_FILE = self.tasks_file

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def read_tasks_file(self):
        if not os.path.exists(self.tasks_file):
            return []
        with open(self.tasks_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_add_and_list(self):
        # add a task
        added = tasks.add_task("Do something")
        self.assertEqual(added["id"], 1)
        self.assertEqual(added["description"], "Do something")

        # file contains one task
        data = self.read_tasks_file()
        self.assertEqual(len(data), 1)
        self.assertFalse(data[0]["completed"])

        # list prints the task
        buf = io.StringIO()
        with redirect_stdout(buf):
            tasks.list_tasks()
        out = buf.getvalue().strip()
        self.assertEqual(out, "1. Do something")

    def test_complete_and_list(self):
        # add two tasks
        tasks.add_task("First")
        tasks.add_task("Second")

        # complete the first
        tasks.complete_task(1)

        # list should only show second
        buf = io.StringIO()
        with redirect_stdout(buf):
            tasks.list_tasks()
        out = buf.getvalue().strip()
        self.assertEqual(out, "2. Second")

    def test_delete(self):
        tasks.add_task("To delete")
        # ensure exists
        data = self.read_tasks_file()
        self.assertEqual(len(data), 1)

        # delete and verify
        tasks.delete_task(1)
        data = self.read_tasks_file()
        self.assertEqual(data, [])


if __name__ == "__main__":
    unittest.main()
