from datetime import datetime, timedelta
from streaks import Streaks

class Habit:
    """
    Allows users to create their own habit
    as part of predefined fitness categories, or as a custom habit.
    """
    def __init__(self):
        self.name = None        # Store habit name
        self.frequency = None   # Stores either daily, weekly, or later custom
        self.creation = None    # Stores the creation date of the habit
        self.completions = []   # Completion dates when the user checks-off a habit
        self.streaks = Streaks()

    def habit_name(self):
        """Prompts the user to name their new habit and confirm it."""
        while True:
            print("What new habit do you want to register?:")
            self.name = input().title()

            # Fail-safe for mistyping
            print(f"You entered '{self.name.title()}'. Is this correct? (yes/no):")
            confirmation = input().lower()

            if confirmation == "yes":
                print(f"You've successfully stored {self.name.title()} as a new habit!")
                break
            elif confirmation == "no":
                print("Let's try again!")

    def habit_frequency(self):
        """Prompts the user to assign their habit's frequency."""
        while True:
            print("Please type in 'Daily' or 'Weekly' to assign your habit's frequency:")
            new_habit_frequency = input().lower()

            if new_habit_frequency in ["daily", "weekly"]:
                self.frequency = new_habit_frequency
                print(f"You've successfully stored {self.frequency} as frequency for {self.name}!")
                break
            else:   # Deals with incorrect input
                print("Please enter either 'Daily' or 'Weekly'!")

    def creation_date(self):
        """Sets the creation date of the habit to the current date."""
        self.creation = datetime.now().date()

    def check_off_habit(self):
        """
        Marks a habit as complete for the current day
        and checks if it has already been completed in the assigned time frequency.
        Returns: False if already completed, True if marked complete.
        """
        current_date = datetime.now()

        if self.frequency == "daily":
            # Check if habit was already completed today
            if current_date.date() in self.completions:
                print(f"'{self.name.title()}' already completed today!")
                return False

            # Add today's date to completions
            self.completions.append(current_date.date())
            print(f"'{self.name.title()}' checked off successfully!")
            self.streaks.calculate_current_streak(self.frequency, self.completions)
            return True

        elif self.frequency == "weekly":
            # Calculate start of the current week (Monday)
            week_start = current_date - timedelta(days=current_date.weekday())
            this_week = []

            for date in self.completions:
                if date >= week_start.date():
                    this_week.append(date)

            if this_week:
                print(f"'{self.name.title()}' already completed this week!")
                return False

            self.completions.append(current_date.date())
            print(f"'{self.name.title()}' checked off successfully!")
            self.streaks.calculate_current_streak(self.frequency, self.completions)
            return True