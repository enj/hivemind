#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple tests for Task."""

import unittest

from hivemind.pipeline import Task
from hivemind.util import tmp_checkpoint_dir


class TestTask(unittest.TestCase):
    """Simple tests."""

    def test_cmd_error(self):
        """Test task with error in command."""
        task = Task("uid", False, False, "does_not_exist", None, ".")
        task._checkpoint_dir = tmp_checkpoint_dir()
        with self.assertRaisesRegexp(RuntimeError, ".*executing Task's command:.*"):
            task.run()
        task.shell = True
        with self.assertRaisesRegexp(RuntimeError, ".*executing Task's command:.*"):
            task.run()
        task._dry_run = True
        task.run()  # No longer raises RuntimeError

    def test_verify_error(self):
        """Test task with error in verification."""
        task = Task("uid", False, False, "echo", "does_not_exist", ".", "A")
        task._checkpoint_dir = tmp_checkpoint_dir()
        with self.assertRaisesRegexp(RuntimeError, ".*executing Task's verification:.*"):
            task.run()
        task.shell = True
        with self.assertRaisesRegexp(RuntimeError, ".*executing Task's verification:.*"):
            task.run()
        task._dry_run = True
        task.run()  # No longer raises RuntimeError

    def test_repr(self):
        """Test task's repr."""
        task = Task("uid", False, False, "", "", "")
        task._pid = 5
        task._rank = 2
        self.assertEqual(repr(task), "uid 5 2")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestTask)
    unittest.TextTestRunner(verbosity=2).run(suite)
