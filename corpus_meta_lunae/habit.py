from datetime import datetime, timedelta
from streaks import Streaks
from helper_functions import confirm_input

class Habit:
    """
    Allows users to create their own habit
    as part of predefined fitness categories, or as a custom habit.
    """
    def __init__(self):
        self.name = None                # Store habit name
        self.frequency = None           # Stores either daily, weekly, or later custom
        self.creation = None            # Stores the creation date of the habit
        self.completions = []           # Completion dates when the user checks-off a habit
        self.streaks = Streaks()

    def habit_name(self):
        """Prompts the user to name their new habit and confirm it."""
        while True:
            print("What new habit do you want to register?:")
            self.name = input().title()
            # Use confirm_input helper function to confirm the habit name
            self.name = confirm_input("name", self.name)

    def habit_frequency(self):
        """Prompts the user to assign their habit's frequency."""
        while True:
            print("Please type in 'Daily' or 'Weekly'")
            self.frequency = input().lower()

            if self.frequency in ["daily", "weekly"]:
                self.frequency = confirm_input("frequency", self.frequency)

            # Handle miss-spelling
            else:
                print("Invalid Input. Pleas enter 'Daily' or 'Weekly'!")

    def creation_date(self):
        """Sets the creation date of the habit to the current date."""
        self.creation = datetime.now().date()

    def _is_habit_completed(self):
        """
        Check if the habit is already completed based on its frequency (daily, weekly).
        :return: True if completed, False otherwise.
        """
        current_date = datetime.now()
        # Calculate start of the current week (Monday)
        week_start = current_date - timedelta(days=current_date.weekday())
        this_week = []

        if self.frequency == "daily":
            # Check if habit was already completed today
            if current_date.date() in self.completions:
                print(f"'{self.name.title()}' already completed today!")
                return True

        elif self.frequency == "weekly":
            for date in self.completions:
                if date >= week_start.date():
                    this_week.append(date)

            if this_week:
                print(f"'{self.name.title()}' already completed this week!")
                return True

        else:
            return False

    def check_off_habit(self):
        """
        Marks a habit as complete for the current day if it hasn't been completed yet.
        :return: False if already completed, True if marked complete.
        """
        current_date = datetime.now()

        # Use the internal helper method to check completion
        if self._is_habit_completed():
            print(f"'{self.name.title()}' has already been completed!")
            return False

        # Add today's date to completions if it's not fully completed
        self.completions.append(current_date.date())
        print(f"'{self.name.title()}' checked off successfully!")

        # Calculate current streak
        self.streaks.calculate_current_streak(self.frequency, self.completions)
        return True