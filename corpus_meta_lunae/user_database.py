import sqlite3
from typing import List
# from pathlib import Path
from .user import User
# from .habit import Habit

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

    def _check_if_table_exists(self) -> None:
        """Ensures the required table exists in the db."""
        connection = self._connect() # Connect to the db
        cursor = connection.cursor() # Create a cursor object to execute SQL commands

        # Create the "users" table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (     
                id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Auto-incrementing id (int) for each user
                username TEXT NOT NULL UNIQUE          -- Username (str) cannot be left empty (NOT NULL) 
            )                                          --   and must be unique
        """)

        # Create the "habits" table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER, 
                name TEXT NOT NULL,
                frequency TEXT NOT NULL,
                creation_date TEXT NOT NULL,
                completions TEXT NOT NULL,
                check_off_dates TEXT NOT NULL, -- Comma separated check off dates
                FOREIGN KEY (user_id) REFERENCES users(id) -- Links habits to a specific user in the user table
            )
        """)

        # Create the "streaks" table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS streaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER, 
            current_streak INTEGER NOT NULL,
            current_streak_start TEXT NOT NULL,
            longest_streak INTEGER NOT NULL,
            longest_streak_start TEXT NOT NULL,
            longest_streak_end TEXT NOT NULL,
            FOREIGN KEY (habit_id) REFERENCES habits(id) -- Link streak to a habit from the habit table
            )
        """)

        connection.commit() # Commit the changes to the db to make sure the tables are created
        connection.close()  # Close the db connection

    def load_users(self) -> List[User]:
        """
        Loads all users from the db.

        :return: A list of User objects.
        """
        connection = self._connect()
        cursor = connection.cursor() # Create a cursor to execute the query

        # Query to select all users from the "users" table
        cursor.execute("SELECT id, username FROM users")
        user_data = cursor.fetchall() # Fetch all rows from the query

        users = [] # An empty list to store User objects

        # Iterate through the fetched data and create User objects
        for user_row in user_data:
            user = User(username=user_row[1]) # Create an object with the username
            users.append(user)

        connection.close()
        return users