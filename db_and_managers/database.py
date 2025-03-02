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

    def delete_user(self, selected_user):
        return user_db.delete_user(selected_user)

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

