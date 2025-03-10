from datetime import datetime, timedelta, date
from typing import List, Optional

from .streaks import Streaks
from helpers.helper_functions import confirm_input, reload_menu_countdown


class Habit:
    """
    Represents a habit that a user wants to track.

    This class handles:
    - creating and checking-off habits
    - tracking completion status

    Attributes:
        name (str): The name of the habit.
        frequency (str): How often the habit should be completed ("daily" or "weekly").
        creation (date): The date when the habit was created.
        completion_dates (List[date]): List of dates when the habit was completed.
        streaks (Streaks): An object to track the streak information for the habit.
    """

    def __init__(self):
        """Initializes a new Habit object with default values."""
        self.name: Optional[str] = None        # Habit name will be set by habit_name()
        self.frequency: Optional[str] = None   # Stores either "daily" or "weekly"
        self.creation: Optional[date] = None   # Set by creation_date()
        self.completion_dates: List[date] = [] # Dates when habit was completed
        self.streaks: Streaks = Streaks()      # Tracks streak information

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
            print("What new habit do you want to register? (Press ENTER to exit): ")
            habit_name = input().title()

            # Exit the loop if "ENTER"
            if not habit_name:
                return

            elif user and habit_name_exists(user, habit_name):
                print(f"A habit named '{habit_name}' already exists! Please try again!")
                reload_menu_countdown()

            else:
                # Confirm the choice
                confirmed_habit = confirm_input("habit", habit_name)

                # If confirmed, set the name and exit the loop
                if confirmed_habit is not None:
                    self.name = confirmed_habit
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
            print(f"Frequency automatically set to {preset_frequency}.")

        # If no preset frequency, prompt the user
        while True:
            print("Please type in 'Daily' or 'Weekly' (Press ENTER to exit): ")
            habit_frequency = input().strip().lower()

            # Exit the loop if empty
            if not habit_frequency:
                return

            # Check if input is valid
            if habit_frequency in ["daily", "weekly"]:
                self.frequency = habit_frequency
                return
            else:
                # Handle invalid input
                print("Invalid Input. Pleas enter 'Daily' or 'Weekly'!")

    def creation_date(self) -> None:
        """Sets the creation date of the habit to the current date."""
        self.creation = datetime.now().date()

    def _is_habit_completed(self, check_date: date=None) -> bool:
        """
        Check if the habit is already completed.

        - for daily habits, checks if completed today
        - for weekly habits, checks if completed this week

        Args:
            check_date: Optional date to check completion for. Defaults to today if None.
        Returns:
            True if already completed, False otherwise.
        """
        if check_date is None:
            check_date = datetime.now().date()

        if self.frequency == "daily":
            # Check if habit was already completed today
            return check_date in self.completion_dates

        elif self.frequency == "weekly":
            # Calculate start of the current week (Monday)
            week_start = check_date - timedelta(days=check_date.weekday())
            # Check if habit was already completed this week
            return any(
                week_start <= completion_date <= week_start + timedelta(days=6)
                for completion_date in self.completion_dates
            )

        return False # If neither condition is met

    def check_off_habit(self, completion_date: date=None) -> bool:
        """
        Marks a habit as complete for the current day.

        - prevents duplicate completion
        - updates streak information upon completion

        Args:
            completion_date: Optional date to mark completion. Defaults to today if None
        Returns:
            True if marked complete, False otherwise.
        """
        if completion_date is None:
            completion_date = datetime.now().date()

        # Use the internal helper method to check completion
        if self._is_habit_completed(completion_date):
            print(f"'{self.name}' has already been completed today!")
            return False

        # Add today's date to completions if it's not already completed
        self.completion_dates.append(completion_date)
        print(f"'{self.name}' completed for today successfully!")

        # Update streaks after the new completion
        self.streaks.get_current_streak(self.frequency, self.completion_dates)
        return True