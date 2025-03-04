from typing import List, Optional

from config import set_db_filepath

from core.user import User
from core.habit import Habit

import manager_user_db as user_db
import manager_habit_db as habit_db

# noinspection PyMethodMayBeStatic
class Database:
    """Coordinator class for the db."""

    def __init__(self, db_filepath: str = "habit_tracker.db") -> None:
        """
        Initializes the Database with a database file path.

        :param db_filepath: Path to the SQLite database file.
        """
        self.db_filepath = db_filepath # Store the filepath as an instance attribute
        self.user_id = None            # Current user's ID (set when a user is selected)
        set_db_filepath(db_filepath)   # Set the global configuration
        # Initialize db tables
        from db_structure import db_tables
        db_tables()

    # Using instance methods for consistent API, despite not using self

    # User related methods
    def load_users(self) -> List[User]:
        """Loads all users from the database."""
        return user_db.load_users()

    def select_user(self) -> Optional[User]:
        """Prompts user to select an existing user or create a new one."""
        selected_user = user_db.select_user()
        if selected_user:
            self.user_id = selected_user.user_id
        return user_db.select_user()

    def delete_user(self, selected_user: User) -> None:
        """Deletes selected user and all their data."""
        return user_db.delete_user(selected_user)

    # Habit related methods
    def load_habits(self, selected_user: User) -> None:
        """Loads all habits for a user."""
        selected_user.habits = habit_db.load_habits(selected_user)

    def add_habit(self, selected_user: User, habit: Habit) -> None:
        """Adds a new habit to the db."""
        habit_db.add_habit(selected_user, habit)

    def save_habits(self, selected_user: User) -> None:
        """Saves all habit modifications for a user."""
        habit_db.save_habits(selected_user)

    def delete_habit(self, selected_user: User, habit: Habit) -> None:
        """Deletes a habit from the user's data."""
        habit_db.delete_habit(selected_user, habit)

    # Completion related methods

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

