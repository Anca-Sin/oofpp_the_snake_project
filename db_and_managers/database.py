from typing import List, Optional

from config import set_db_filepath
from core.user import User
from core.habit import Habit
from helpers.helper_functions import cancel_operation
from .db_structure import db_tables
from db_and_managers import manager_user_db as user_db
from db_and_managers import manager_habit_db as habit_db
from db_and_managers import manager_completion_db as completion_db

# noinspection PyMethodMayBeStatic
class Database:
    """
    Central coordinator - single entry point - for all database operations.

    - ONLY methods needed for app functionality (managers handle other necessary functions internally)
    - exclusively manages all data synchronization needed for app functionality

    Attributes:
        db_filepath: A string representing the path to the SQLite database file.
        user_id: An integer representing the ID of the currently selected user.
    """

    def __init__(self, db_filepath: str = "habit_tracker.db") -> None:
        """Initializes the Database connection and tables."""
        self.db_filepath = db_filepath # Store the filepath as an instance attribute
        self.user_id = None            # Current user's ID (set when a user is selected)
        set_db_filepath(db_filepath)   # Set the global configuration

        # Initialize db tables
        db_tables()

    # All methods delegate to their respective manager modules to handle the db operations

    # --------------------
    # User related methods
    # --------------------
    def load_users(self) -> List[User]:
        """
        Loads all users from the db.

        Returns:
            A list of User objects.
        """
        users = user_db.load_users()
        return users

    def save_user(self, selected_user) -> None:
        """
        Saves a user to the database.

        Args:
            selected_user: The User object to save.
        """
        user_db.save_user(selected_user)

    def select_user(self) -> Optional[User]:
        """
        Performs multiple steps logic:
        - loads the users from the database
        - delegates user selection/creation to the manager function
        - sets the user id for further db operations
        - loads the selected user's habits
        - handles operation canceling

        Returns:
             The selected User object if the process isn't canceled.
        """
        while True:
            users = self.load_users()
            selected_user = user_db.select_user(users)
            if selected_user is not None:
                if selected_user:
                    if selected_user.user_id is None:
                        self.save_user(selected_user)

                    self.user_id = selected_user.user_id

                    self.load_habits(selected_user)

                return selected_user
            else:
                cancel_operation("User creation process")

    def delete_user(self, selected_user: User) -> None:
        """
        Performs multiple steps logic:
        - deletes the selected user and all their data from the db through manager function
        - refreshes the existing users after deletion
        - opens up the logic in select_user

        Args:
            selected_user: The User object to be deleted.
        """
        user_db.delete_user(selected_user)
        # Refresh users list
        self.load_users()
        # Back to user selection
        self.select_user()

    # ---------------------
    # Habit related methods
    # ---------------------
    def load_habits(self, selected_user: User) -> List[Habit]:
        """
        Loads all habits for the selected user from the db.

        Args:
            selected_user: The User object whose habits are to be loaded.
        Returns:
            A list of Habit objects for the selected user.
        """
        selected_user.habits = habit_db.load_habits(selected_user)
        return selected_user.habits

    def save_habits(self, selected_user, new_habit=None) -> None:
        """
        Saves habit data to the database.

        Args:
            selected_user: The User object whose habits to save.
            new_habit:     If provided, saves only this new habit.
                           Otherwise, updates all habits data for the user.
        """
        habit_db.save_habits(selected_user, new_habit)

    def new_habit(self, selected_user: User, set_frequency: str = None) -> Optional[Habit]:
        """
        Adds a new habit to the db for the selected user.

        Args:
            selected_user: The User object to associate the new habit with.
            set_frequency: Optional preset frequency for the habit ("daily" or "weekly").
        """
        new_habit = habit_db.new_habit(selected_user, set_frequency)
        # Check if the new habit was created successfully, and process wasn't canceled
        if new_habit is not None:
            # Save
            self.save_habits(selected_user, new_habit=new_habit)
            # Refresh habits list
            self.load_habits(selected_user)
            return new_habit
        else:
            cancel_operation("Habit creation process")
            return None

    def delete_habit(self, selected_user: User, habit: Habit) -> None:
        """
        Deletes a habit and all associated data from the database.

        Args:
            selected_user: The User object whose habit is to be deleted.
            habit: The Habit object to be deleted.
        """
        habit_db.delete_habit(selected_user, habit)
        # Refresh habits list
        self.load_habits(selected_user)

    # --------------------------
    # Completion related methods
    # --------------------------
    def complete_habit_today(self, selected_user: User, habit: Habit) -> None:
        """
        Marks a habit as complete for the current day.

        Args:
            selected_user: The User object whose habit is to be completed.
            habit: The Habit object to be completed.
        """
        completion = completion_db.complete_habit_today(habit)
        if completion:
            habit.completion_dates.append(completion)
            habit.streaks.get_current_streak(habit.frequency, habit.completion_dates)
            self.save_habits(selected_user)

    def complete_habit_past(self, selected_user: User, habit: Habit) -> None:
        """
        Marks the selected habit as complete for a past date.

        Args:
            selected_user: The User object whose habit is to be completed.
            habit: The Habit object to be completed.
        """
        completion = completion_db.complete_habit_past(habit)
        if completion:
            habit.completion_dates.append(completion)
            habit.streaks.get_current_streak(habit.frequency, habit.completion_dates, completion)
            self.save_habits(selected_user)


    def delete_completion(self, selected_user: User, habit: Habit) -> None:
        """
        Deletes a completion for the selected habit.

        Args:
            selected_user: The User object which owns the habit.
            habit: The Habit object whose completion is to be completed.
        """
        deletion = completion_db.delete_completion(habit)
        if deletion:
            habit.completion_dates.remove(deletion)
            habit.streaks.get_current_streak(habit.frequency, habit.completion_dates, deletion)
            self.save_habits(selected_user)