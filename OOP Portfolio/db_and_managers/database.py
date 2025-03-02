import sqlite3
from typing import List
from core.user import User
from db_and_managers.database import Database
from helper_functions import confirm_int_input, reload_menu_countdown


class Database:
    """Handles saving and loading user data to/from an SQLite database."""

    def __init__(self, db_filepath: str = "habit_tracker.db") -> None:
        """
        Initializes the Database with a database file path.

        :param db_filepath: Path to the SQLite database file.
        """
        self.db_filepath = db_filepath
        self._access_db_tables()

    def connect(self) -> sqlite3.Connection:
        """Establishes a connection to the SQLite database."""
        # sqlite3.connect() -> opens a connection to the SQLite database
        return sqlite3.connect(self.db_filepath)

    def _access_db_tables(self) -> None:
        """Establishes a connection to the SQLite db for further interactions."""
        connection = self.check_db_connection() # Upcoming helper function

        db_tables(connection) # Access the tables

        connection.close()

    def load_users(self) -> List[User]:
        """
        Loads all users from the db.

        :return: A list of User objects.
        """
        connection = self.connect()
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

    def save_user(self, user: User) -> int: # Return the user_id to set faster connections, eliminating an extra query.
        """
        Saves a user to the db if it doesn't already exist.

        :param user: The User object to save.
        :return: The user_id from the db.
        """
        connection = self.connect()
        cursor = connection.cursor()

        # Check if the user exists
        cursor.execute("SELECT id FROM users WHERE username = ?", (user.username,))
        user_row = cursor.fetchone()

        if user_row:
            # Return the existing user's id
            user_id = user_row[0]
        else:
            # Insert new user
            cursor.execute("INSERT INTO users (username) VALUES (?)", (user.username,))
            user_id = cursor.lastrowid
            connection.commit()

        connection.close()
        return user_id

    def select_user(self) -> User:
        """
        Prompts the user to select an existing user or create a new one if none exists.

        :return: The selected or newly created User object.
        """
        # Load all users
        users = self.load_users()

        # If there are no users, directly prompt to create a new user
        if not users:
            print("""No users found!
            You need to create a new user!""")
            selected_user = User()
            selected_user.create_username()
            self.save_user(selected_user)
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
                    self.save_user(selected_user)
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

    def delete_user(self, current_user) -> None:
        """Deletes an user and all associated data."""
        # Ask for confirmation
        print(f"""This will delete:
        - your username
        - all associated habits and data
        
        """)
        confirmation = input("Type in 'yes' if you are sure to proceed: ")

        if confirmation.lower() != "yes":
            print("Deletion canceled.")
            reload_menu_countdown()
            return

        connection = self.connect()
        cursor = connection.cursor()

        # Get the current user's ID
        cursor.execute("SELECT id FROM users WHERE username = ?", (current_user.username,))
        user_id = cursor.fetchone()[0]

        # Get all habit IDs for this user
        cursor.execute("SELECT id FROM habit WHERE user_id = ?", (user_id,))
        habit_ids = [row[0] for row in cursor.fetchall()]

        # Delete streak records
        for habit_id in habit_ids:
            cursor.execute("DELETE FROM streaks WHERE habit_id = ?", (habit_id,))

        # Delete habits
        cursor.execute("DELETE FROM habits WHERE user_id = ?", (user_id,))

        # Delete user
        cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))

        connection.commit()
        connection.close()

        print(f"User '{current_user.username}' and all associated data have been deleted.")
        reload_menu_countdown()

    def save_habits(self, user: User) -> None:

    def complete_habit_today()
    def complete_habit_past()
    def delete_completion()
    def delete_habit()

    def save_broken_streak_length(self, habit_name: str, streak_length: int) -> None:
        """
        When a streak is broken, this method records the length and stores it the db.

        :param habit_name: The name of the habit whose streak was broken.
        :param streak_length: The length of the streak that was broken.
        """
        connection = self.connect()
        cursor = connection.cursor()

        # Retrieve the current streak_length_history for the habit
        cursor.execute("SELECT streak_length_history FROM streaks WHERE habit_name = ?", (habit_name,))
        result = cursor.fetchone()

        if result[0]: # If there's an existing streak history
            streak_history = result[0] + f",{streak_length}" # Append the new streak length
        else: # If no streak history exists
            streak_history = str(streak_length) # Initialize it

        # Update the streak_length history in the db
        cursor.execute("""
            UPDATE streaks
            SET streak_length_history = ?
            WHERE habit_name = ?
        """, (streak_history, habit_name))

        connection.commit()
        connection.close()

    def load_broken_streak_length(self, habit_name: str) -> str:
        """
        Loads streak_length_history for a given habit from the db.

        :param habit_name:
        :return: The broken streaks' lengths as a list of integers.
        """
        connection = self.connect()
        cursor = connection.cursor()

        # Retrieve the streak_length_history for the given habit
        cursor.execute("SELECT streak_length_history FROM streaks WHERE habit_name = ?", (habit_name,))
        result = cursor.fetchone()

        connection.close()

        # If streak_length_history is empty or NULL
        if not result[0]:
            return "" # Return an empty string
        else:
            return result[0] # Return the streak_length_history string

