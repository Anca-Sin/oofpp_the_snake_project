from typing import List

from config import set_db_filepath

from core.user import User
from helpers.helper_functions import reload_menu_countdown

import manager_user_db as user_db

# noinspection PyMethodMayBeStatic
class Database:
    """Coordinator class for the db."""

    def __init__(self, db_filepath: str = "habit_tracker.db") -> None:
        """
        Initializes the Database with a database file path.

        :param db_filepath: Path to the SQLite database file.
        """
        self.db_filepath = db_filepath # Store the filepath as an instance attribute
        set_db_filepath(db_filepath)   # Set the global configuration
        # Initialize db tables
        from db_structure import db_tables
        db_tables()

    # Using instance methods for consistent API, despite not using self

    def load_users(self) -> List[User]:
        return user_db.load_users()

    def select_user(self) -> User:
        return user_db.select_user()

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
        pass

    def complete_habit_today(self):
        pass

    def complete_habit_past(self):
        pass
    def delete_completion(self):
        pass
    def delete_habit(self):
        pass

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

