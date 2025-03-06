from datetime import datetime, timedelta, date
from typing import List, Optional

from .streaks import Streaks
from helpers.helper_functions import confirm_input

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
        """
        Initializes a new Habit object with default values.
        """
        self.name: Optional[str] = None        # Habit name will be set by habit_name()
        self.frequency: Optional[str] = None   # Stores either "daily" or "weekly"
        self.creation: Optional[date] = None   # Set by creation_date()
        self.completion_dates: List[date] = [] # Dates when habit was completed
        self.streaks: Streaks = Streaks()      # Tracks streak information

    def habit_name(self) -> None:
        """
        Prompts the user to name their new habit and confirm it.


        """
        while True:
            print("What new habit do you want to register? (Press ENTER to exit): ")
            habit_name = input().strip().title()

            # Exit the loop if empty
            if not habit_name:
                return

            # Confirm the choice through helper method
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

    def _is_habit_completed(self) -> bool:
        """
        Check if the habit is already completed.

        - for daily habits, checks if completed today
        - for weekly habits, checks if completed this week

        Returns:
            bool: True if already completed, False otherwise.
        """
        current_date = datetime.now()

        if self.frequency == "daily":
            # Check if habit was already completed today
            return current_date.date() in self.completion_dates

        elif self.frequency == "weekly":
            # Calculate start of the current week (Monday)
            week_start = current_date - timedelta(days=current_date.weekday())
            # Check if habit was already completed this week
            return any(completion_date >= week_start.date() for completion_date in self.completion_dates)

        return False # If neither condition is met

    def check_off_habit(self) -> bool:
        """
        Marks a habit as complete for the current day.

        - prevents duplicate completion
        - updates streak information upon completion

        Returns:
            bool: True if marked complete, False otherwise.
        """
        current_date = datetime.now()

        # Use the internal helper method to check completion
        if self._is_habit_completed():
            print(f"'{self.name.title()}' has already been completed!")
            return False

        # Add today's date to completions if it's not already completed
        self.completion_dates.append(current_date.date())
        print(f"'{self.name.title()}' completed for today successfully!")

        # Calculate current streak based on completion history
        self.streaks.get_current_streak(self.frequency, self.completion_dates)
        return True