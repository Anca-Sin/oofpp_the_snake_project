from typing import List, Optional

from config import set_db_filepath

from core.user import User
from core.habit import Habit

from .db_structure import db_tables
from db_and_managers import manager_user_db as user_db
from db_and_managers import manager_habit_db as habit_db
from db_and_managers import manager_completion_db as completion_db
from db_and_managers import manager_streaks_db as streaks_db
from .manager_user_db import load_users


# noinspection PyMethodMayBeStatic
class Database:
    """
    Coordinator class for database operations.
    This class is a placeholder for specialized manager modules which delegate specific functionalities.

    - initializes the db structure
    - provides a common space for the application to interact with the database

    Attributes:
        db_filepath (str): Path to the SQLite database file, defaults to "habit_tracker" through config.
        user_id (int): ID of the currently selected user.
    """


    def __init__(self, db_filepath: str = "habit_tracker.db") -> None:
        """Initializes the Database."""
        self.db_filepath = db_filepath # Store the filepath as an instance attribute
        self.user_id = None            # Current user's ID (set when a user is selected)
        set_db_filepath(db_filepath)   # Set the global configuration

        # Initialize db tables
        db_tables()

    # All methods delegate to their respective manager modules to handle the db operations

    # User related methods
    def load_users(self) -> List[User]:
        """
        Loads all users from the database.

        Returns:
             A list of User objects retrieved from the db.
        """
        return user_db.load_users()

    def select_user(self) -> Optional[User]:
        """
        Prompts user to select an existing user or create a new one.

        Returns:
             The selected User object, or None if no selection is made.
        """
        selected_user = user_db.select_user()
        if selected_user:
            self.user_id = selected_user.user_id
        return selected_user

    def save_user(self, user: User) -> None:
        """
        Saves a new user to the db.

        Args:
             The User object to be saved.
        """
        return user_db.save_user(user)

    def delete_user(self, selected_user: User) -> None:
        """
        Deletes the selected user and all their data from the db.

        Args:
            selected_user: The User object to be deleted.
        """
        return user_db.delete_user(selected_user)

    # Habit related methods
    def load_habits(self, selected_user: User) -> None:
        """
        Loads all habits for the selected user from the db.

        Args:
            selected_user: The User object whose habits are to be loaded.
        """
        selected_user.habits = habit_db.load_habits(selected_user)

    def new_habit(self, selected_user: User, set_frequency: str = None) -> None:
        """
        Adds a new habit to the db for the selected user.

        Args:
            selected_user: The User object to associate the new habit with.
            set_frequency: Optional preset frequency for the habit ("daily" or "weekly").
        """
        habit_db.new_habit(selected_user, set_frequency)

    def save_habits(self, selected_user: User, new_habit=None) -> None:
        """
        Saves or updates all habit modifications for the selected user in the db.

        Args:
            selected_user: The User object whose habits to save/update.
            new_habit
        """
        habit_db.save_habits(selected_user, new_habit)

    def delete_habit(self, selected_user: User, habit: Habit) -> None:
        """
        Deletes a habit from the user's data.

        Args:
            selected_user: The User object whose habit is to be deleted.
            habit: The Habit object to be deleted.
        """
        habit_db.delete_habit(selected_user, habit)

        # Refresh habits list
        self.load_habits(selected_user)

    # Completion related methods
    def complete_habit_today(self, selected_user: User, habit: Habit) -> None:
        """
        Marks the selected habit as complete for today.

        Args:
            selected_user: The User object whose habit is to be completed.
            habit: The Habit object to be completed.
        """
        completion_db.complete_habit_today(selected_user, habit)

    def complete_habit_past(self, selected_user: User, habit: Habit) -> None:
        """
        Marks the selected habit as complete for a past date.

        Args:
            selected_user: The User object whose habit is to be completed.
            habit: The Habit object to be completed.
        """
        completion_db.complete_habit_past(selected_user, habit)

    def delete_completion(self, selected_user: User, habit: Habit) -> None:
        """
        Deletes a completion for the selected habit.

        Args:
            selected_user: The User object associated with the habit.
            habit: The Habit object whose completion is to be completed.
        """
        completion_db.delete_completion(selected_user, habit)

    # Streak related methods
    def load_broken_streak_lengths(self, habit_name: str) -> str:
        """
        Loads broken streak length history for a given habit.

        Args:
            habit_name: Name of the habit
        Returns:
            A comma separated string of broken streak lengths.
        """
        return streaks_db.load_broken_streak_lengths(habit_name)