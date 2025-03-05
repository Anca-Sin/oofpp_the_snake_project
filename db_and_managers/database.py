from typing import List, Optional

from config import set_db_filepath

from core.user import User
from core.habit import Habit

import manager_user_db as user_db
import manager_habit_db as habit_db
import manager_completion_db as completion_db
import manager_streaks_db as streaks_db

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
        return selected_user

    def delete_user(self, selected_user: User) -> None:
        """Deletes selected user and all their data."""
        return user_db.delete_user(selected_user)

    # Habit related methods
    def load_habits(self, selected_user: User) -> None:
        """Loads all habits for a user."""
        selected_user.habits = habit_db.load_habits(selected_user)

    def new_habit(self, selected_user: User, habit: Habit) -> None:
        """Adds a new habit to the db."""
        habit_db.new_habit(selected_user, habit)

    def save_habits(self, selected_user: User) -> None:
        """Saves all habit modifications for a user."""
        habit_db.save_habits(selected_user)

    def delete_habit(self, selected_user: User, habit: Habit) -> None:
        """Deletes a habit from the user's data."""
        habit_db.delete_habit(selected_user, habit)

    # Completion related methods
    def complete_habit_today(self, selected_user: User, habit: Habit) -> None:
        """Marks a habit as complete for today."""
        completion_db.complete_habit_today(selected_user, habit)

    def complete_habit_past(self, selected_user: User, habit: Habit) -> None:
        """Marks a habit as complete for a past date."""
        completion_db.complete_habit_past(selected_user, habit)

    def delete_completion(self, selected_user: User, habit: Habit) -> None:
        """Deletes a completion for a habit."""
        completion_db.delete_completion(selected_user, habit)

    # Streak related methods
    def load_broken_streak_length(self, habit_name: str) -> str:
        """
        Loads broken streak length history for a given habit.

        :param habit_name: Name of the habit
        :return: Comma separated string of broken streak lengths.
        """
        return streaks_db.load_broken_streak_length(habit_name)