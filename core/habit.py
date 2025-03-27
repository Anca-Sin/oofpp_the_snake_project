import time
from datetime import datetime, date
from typing import List, Optional

from .streaks import Streaks
from helpers.helper_functions import confirm_input, enter, invalid_input
from helpers.text_formating import GRAY, RES, RED


class Habit:
    """
    A habit registered by a selected user.
    Represents a trackable habit with its required properties for the application.

    - interacts with the user to:
            - handle habit name creation
            - set habit periodicity (if no preset is provided)
    - has no direct db dependency:
              habits are directly linked to their user through foreign keys relationships in the db tables
    - stores:
            - the creation date of a new habit
            - a list of dates when a habit was completed by the user
    - initializes its own Streak instance for streak calculations

    Attributes:
        name:             A string assigned by the user.
        frequency:        A string determining how often the habit should be completed ("daily" or "weekly").
        creation_date:    A date stored when a new habit name is registered.
        completion_dates: A list of dates when a habit was completed by the user.
        streaks:          A Streaks instance which calculates streak information for a habit.
    """

    def __init__(self):
        """Initializes the Habit instance."""
        self.name: Optional[str] = None
        self.frequency: Optional[str] = None
        self.creation_date: Optional[date] = None
        self.completion_dates: List[date] = []
        self.streaks: Streaks = Streaks()

    def habit_name(self, user=None) -> None:
        """
        Handles the creation of a new habit name.

        - prompts for user input
        - validates against existing habit names in the database
        - handles confirmation through helper function
        - sets the name attribute if successful, or None if canceled

        Args:
            user: The entity which owns the habit.
        """
        # Avoid circular imports
        from db_and_managers.manager_habit_db import habit_name_exists

        while True:
            # Ask for habit name
            habit_name = input(
                f"\nNew habit name or {enter()} to exit: "
            ).title().strip()

            # Exit the loop if << ENTER
            if not habit_name:
                self.name = None
                return # Cancels the process

            # Check if habit name already exists (using habit db manager function)
            elif habit_name_exists(user, habit_name):
                print(f"\nHabit '{habit_name}' {RED}already{RES} exists!")
                time.sleep(1)

            # If habit name is valid
            elif habit_name is not None:
                # Confirm the choice
                confirmed_habit = confirm_input("new habit name", habit_name)

                # If confirmed, set the name and exit the loop
                if confirmed_habit is not None:
                    self.name = confirmed_habit
                    return

                # If not confirmed << ENTER
                else:
                    return

    def habit_frequency(self, preset_frequency: Optional[str] = None) -> None:
        """
        Sets the habit's frequency:
        - by prompting the user
        or
        - using a preset value

        Args:
            preset_frequency: If provided, skips prompting the user.
                              Is set when a new habit is created from listing all daily or weekly habits when none exist.
        """
        # If preset frequency is provided, assign it without prompting
        if preset_frequency in ["daily", "weekly"]:
            self.frequency = preset_frequency
            print(f"\nFrequency automatically set to {preset_frequency}.")
            return

        # If no preset frequency, prompt the user
        while True:
            habit_frequency = input(
                f"\nType 'Daily' or 'Weekly' or {enter()} to exit: "
            ).strip().lower()

            # Exit the loop if "ENTER"
            if not habit_frequency:
                self.frequency = None
                return

            # Check if input is valid
            if habit_frequency in ["daily", "weekly"]:
                self.frequency = habit_frequency
                return

            # Handle invalid input with user feedback
            else:
                invalid_input()

    def create_date(self) -> None:
        """Sets the creation date of the habit to the current date."""
        self.creation_date = datetime.now().date()