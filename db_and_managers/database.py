import time
from typing import List, Optional

from config import set_db_filepath

from core.user import User
from core.habit import Habit
from helpers.colors import RED, RES
from helpers.helper_functions import db_connection

from .db_structure import db_tables
from db_and_managers import manager_user_db as user_db
from db_and_managers import manager_habit_db as habit_db
from db_and_managers import manager_completion_db as completion_db

# noinspection PyMethodMayBeStatic
class Database:
    """
    Coordinator class - SINGLE app entry point - for database operations.

    - ONLY methods needed for app functionality (managers handle other necessary functions internally)
    - initializes the db structure
    - handles ALL data synchronization needed for app functionality
    - manages exclusively all database changes through manager's functional operation

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

    def save_user(self, selected_user):
        """ok"""
        user_db.save_user(selected_user)

    def select_user(self) -> Optional[User]:
        """
        - loads the users from the database
        - delegates user selection/creation to the manager function
        - sets the user id for further db operations
        - loads the selected user's habits

        Returns:
             The selected User object.
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
                print(f"User creation process {RED}canceled!{RES}")
                time.sleep(1)
                print("\nNo changes will be saved...")
                time.sleep(1)
                print("\nReturning...")
                time.sleep(1)

    def delete_user(self, selected_user: User) -> None:
        """
        - deletes the selected user and all their data from the db through manager function
        -
        Args:
            selected_user: The User object to be deleted.
        """
        user_db.delete_user(selected_user)

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

    def save_habits(self, selected_user, new_habit=None):
        """ok"""
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
            print(f"Habit creation process {RED}canceled!{RES}")
            time.sleep(1)
            print("\nNo changes will be saved...")
            time.sleep(1)
            print("\nReturning...")
            time.sleep(1)
            return None

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

    # --------------------------
    # Completion related methods
    # --------------------------
    def complete_habit_today(self, selected_user: User, habit: Habit) -> None:
        """
        Marks the selected habit as complete for today.

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
            selected_user: The User object associated with the habit.
            habit: The Habit object whose completion is to be completed.
        """
        deletion = completion_db.delete_completion(habit)
        if deletion:
            habit.completion_dates.remove(deletion)
            habit.streaks.get_current_streak(habit.frequency, habit.completion_dates, deletion)
            self.save_habits(selected_user)

    # ----------------------
    # Streaks related method
    # ----------------------
    def load_broken_streak_lengths(self, habit_name: str) -> str:
        """
        Loads streak_length_history for a given habit from the db.

        - retrieves the history of broken streak lengths for a selected habit
        - streak_length_history is initialized as an empty string when creating a habit,
                                                so it will always return a valid string

        Args:
            habit_name: The name of the habit to get the streak history for.
        Returns:
            The broken streaks' lengths as a comma separated string.
            An empty string if no history exists.
        """
        connection = db_connection(self.db_filepath)
        cursor = connection.cursor()

        # Retrieve the streak_length_history for the selected habit
        cursor.execute("""
            SELECT streak_length_history
            FROM streaks
            JOIN habits ON streaks.habit_id = habits.id
            WHERE habits.habit_name = ?
        """, (habit_name,))

        # Get result
        result = cursor.fetchone()
        connection.close()

        # Will return empty string if no history
        return result[0]