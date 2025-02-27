import sqlite3
from typing import List

from .helper_functions import confirm_int_input
# from pathlib import Path
from .user import User
# from .habit import Habit
import helper_functions

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
                habit_name TEXT NOT NULL,
                frequency TEXT NOT NULL,
                creation_date TEXT NOT NULL,
                completions_count INTEGER, -- Count of completions
                checked_off_dates TEXT, -- Comma separated check off dates
                FOREIGN KEY (user_id) REFERENCES users(id) -- Links habits to a specific user in the user table
            )
        """)

        # Create the "streaks" table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS streaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER, 
            current_streak INTEGER,
            current_streak_start TEXT,
            longest_streak INTEGER,
            longest_streak_start TEXT,
            longest_streak_end TEXT,
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

    def select_user(self) -> User:
        """
        Prompts the user to select an existing user or create a new one if none exists.

        :return: The selected or newly created User object.
        """
        # Load all users
        users = self.load_users()

        # If there are no users, directly prompt to create a new user
        if not users:
            print("No users found!")
            selected_user = User()
            selected_user.create_username()
            return selected_user

        # Display the users to choose from
        print("Please select a user from the following list: ")
        for idx, user in enumerate(users, 1):
            print(f"{idx}. {user.username}")

        # Or allow for a new user creation
        print("Or type in 'new' to create a new user!")

        # Ask user for a choice
        while True:
            try:
                choice = input(f"Enter a number between 1 and {len(users)} or type in 'new': ").strip()

                if choice.lower() == "new":
                    selected_user = User()
                    selected_user.create_username()
                    return selected_user
                elif choice.isdigit() and 1 <= int(choice) <= len(users):
                    # Confirm the choice
                    confirmed_choice = confirm_int_input(choice)

                    if confirmed_choice is not None:
                        # If the choice was confirmed, get the corresponding user
                        selected_user = users[int(confirmed_choice) - 1] # Adjust index since user listing starts from 1
                        print(f"You've selected: {selected_user.username}")
                        break
                    # If choice wasn't confirmed, the loop will execute again asking for a user index
                else:
                    print(f"Invalid selection! Please enter a number between 1 and {len(users)}, or 'new': ")

            except ValueError: # Handle invalid input
                print(f"Invalid input! Please enter a number between 1 and {len(users)} or 'new': ")

        return selected_user

    # def save_habits(self, user: User) -> None:
    #     """Saves or updates the user's habits in the db."""
    #     connection = self._connect()
    #     cursor = connection.cursor()
    #
    #     for habit in user.habits:
    #         # Convert completion_dates list into a comma-separated string
    #         checked_off_dates = ",".join(str(date) for date in habit.completion_dates)
    #
    #         # Count how many times the habit has been completed
    #         completions_count = len(habit.completion_dates)