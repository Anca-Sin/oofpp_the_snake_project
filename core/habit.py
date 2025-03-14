from datetime import datetime, date
from typing import List, Optional

from .streaks import Streaks
from helpers.helper_functions import confirm_input, reload_menu_countdown
from helpers.colors import GRAY, RES


class Habit:
    """
    Represents a user's habit.

    - handles habit name creation and periodicity setting
    - has no direct db dependency:
            habits are directly linked to their user through foreign keys relationships in the db

    Attributes:
        name (str): The name of the habit.
        frequency (str): How often the habit should be completed ("daily" or "weekly").
        creation_date (date): The date when the habit was created.
        completion_dates (List[date]): List of dates when the habit was completed.
        streaks (Streaks): A Streak instance tracking streak information for the habit.
    """

    def __init__(self):
        """Initializes a new Habit object with default values."""
        self.name: Optional[str] = None             # Habit name will be set by habit_name()
        self.frequency: Optional[str] = None        # Stores either "daily" or "weekly"
        self.creation_date: Optional[date] = None   # Set by creation_date()
        self.completion_dates: List[date] = []      # Dates when habit was completed
        self.streaks: Streaks = Streaks()           # Tracks streak information for a given habit

    def habit_name(self, user=None) -> None:
        """
        Creates a new habit name.

        - handles input and confirmation
        - checks if the habit name already exists in the db

        Args:
            user: The User object to check for existing habit names.
        """
        # Avoid circular imports
        from db_and_managers.manager_habit_db import habit_name_exists

        while True:
            # Ask for habit name
            print(f"\nNew Habit name {GRAY}or ENTER << to exit:{RES} ")
            habit_name = input().title().strip()

            # Exit the loop if "ENTER"
            if not habit_name:
                self.name = None
                return

            elif habit_name_exists(user, habit_name):
                print(f"\nA habit named '{habit_name}' already exists! Please try again!")
                reload_menu_countdown()
                return

            elif habit_name is not None:
                # Confirm the choice
                confirmed_habit = confirm_input("new habit name", habit_name)

                # If confirmed, set the name and exit the loop
                if confirmed_habit is not None:
                    self.name = confirmed_habit
                    return
                else:
                    # If confirmed input is None on << ENTER
                    return

    def habit_frequency(self, preset_frequency: Optional[str] = None) -> None:
        """
        Sets the habit's frequency either by:
        - prompting the user
        - using a preset value

        Args:
            preset_frequency: Optional preset frequency value ("daily" or "weekly).
                              If provided, skips prompting the user.
        """
        # If preset frequency is provided, assign it without prompting
        if preset_frequency in ["daily", "weekly"]:
            self.frequency = preset_frequency
            print(f"\nFrequency automatically set to {preset_frequency}.")
            return

        # If no preset frequency, prompt the user
        while True:
            print(f"\nPlease type in 'Daily' or 'Weekly' {GRAY}or ENTER << to exit{RES}: ")
            habit_frequency = input().strip().lower()

            # Exit the loop if "ENTER"
            if not habit_frequency:
                self.frequency = None
                return

            # Check if input is valid
            if habit_frequency in ["daily", "weekly"]:
                # Confirm the choice
                confirmed_frequency = confirm_input("frequency", habit_frequency)

                # If confirmed, set the name and exit the loop
                if confirmed_frequency is not None:
                    self.frequency = confirmed_frequency
                    return
                else:
                    # If confirmed input is None on << ENTER
                    return

            else:
                # Handle invalid input
                print("\nInvalid Input. Please enter 'Daily' or 'Weekly'!")

    def creation_date(self) -> None:
        """Sets the creation date of the habit to the current date."""
        self.creation_date = datetime.now().date()