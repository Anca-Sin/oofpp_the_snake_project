import sqlite3
from pathlib import Path
from typing import List, cast, Any
from .user import User
from .habit import Habit

class UserDatabase:
    """Handles saving and loading user data to/from an SQLite database."""

    def __init__(self, db_filepath: str = "habit_tracker.db") -> None:
        """
        Initializes the UserDatabase with a database file path.

        :param db_filepath: Path to the SQLite database file.
        """
        self.db_filepath = db_filepath

    def _connect(self) -> sqlite3.Connection:
        """Establishes a connection to the SQLite database."""
        # sqlite3.connect() -> opens a connection to the SQLite database
        # If the db doesn't exist it will be created automatically
        return sqlite3.connect(self.db_filepath)

