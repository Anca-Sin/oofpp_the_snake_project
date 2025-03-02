from datetime import datetime, timedelta, date
from .streaks import Streaks
from helpers.helper_functions import confirm_input
from typing import List, Optional

class Habit:
    """
    Allows users to create their own habit
    as part of predefined fitness categories, or as a custom habit.
    """

    def __init__(self):
        self.name: Optional[str] = None        # Store habit name
        self.frequency: Optional[str] = None   # Stores either daily, weekly, or later custom
        self.creation: Optional[date] = None   # Stores the creation date of the habit
        self.completion_dates: List[date] = [] # List of completion dates when the user checks-off a habit
        self.streaks: Streaks = Streaks()      # Streaks object (instance of Streaks class)

    def habit_name(self) -> None:
        """Prompts the user to name their new habit and confirm it."""
        while True:
            print("What new habit do you want to register?:")
            habit_name = input().title()
            # Confirm the choice
            confirmed_habit = confirm_input("habit", habit_name)

            if confirmed_habit is not None:
                self.name = confirmed_habit
                return

    def habit_frequency(self) -> None:
        """Prompts the user to assign their habit's frequency."""
        while True:
            print("Please type in 'Daily' or 'Weekly'")
            habit_frequency = input().lower()

            if habit_frequency in ["daily", "weekly"]:
                # Confirm the choice
                confirmed_frequency = confirm_input("frequency", habit_frequency)

                if confirmed_frequency is not None:
                    self.frequency = confirmed_frequency
                    return

            # Handle miss-spelling
            else:
                print("Invalid Input. Pleas enter 'Daily' or 'Weekly'!")

    def creation_date(self) -> None:
        """Sets the creation date of the habit to the current date."""
        self.creation = datetime.now().date()

    def _is_habit_completed(self) -> bool:
        """
        Check if the habit is already completed based on its frequency ("daily" or "weekly").

        :return: True if completed, False otherwise.
        """
        current_date = datetime.now()
        # Calculate start of the current week (Monday)
        week_start = current_date - timedelta(days=current_date.weekday())

        if self.frequency == "daily":
            # Check if habit was already completed today
            return current_date.date() in self.completion_dates

        elif self.frequency == "weekly":
            # Check if habit was already completed this week
            return any(completion_date >= week_start.date() for completion_date in self.completion_dates)

        return False # If neither condition is met

    def check_off_habit(self) -> bool:
        """
        Marks a habit as complete for the current day if it hasn't been completed yet.

        :return: False if already completed, True if marked complete.
        """
        current_date = datetime.now()

        # Use the internal helper method to check completion
        if self._is_habit_completed():
            print(f"'{self.name.title()}' has already been completed!")
            return False

        # Add today's date to completions if it's not already completed
        self.completion_dates.append(current_date.date())
        print(f"'{self.name.title()}' checked off successfully!")

        # Calculate current streak
        self.streaks.calculate_current_streak(self.frequency, self.completion_dates)
        return True