"""
Here how we want to change our TodoApp object to support persistence
"""

import unittest
import tempfile
from pathlib import Path

from todo.app import TodoApp


class TestTodoApp(unittest.TestCase):
    """
    describes if app can accept a DB path and that if omitted, it should use the current dir
    """
    def test_default_dbpath(self):
        app = TodoApp()
        assert Path(".").resolve() == Path(app._dbpath).resolve()

    def test_accepts_dbpath(self):
        expected_path = Path(tempfile.gettempdir(), "something")
        app = TodoApp(dbpath=str(expected_path))
        assert expected_path == Path(app._dbpath)
