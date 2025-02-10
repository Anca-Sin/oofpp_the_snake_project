from datetime import datetime, timedelta

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
        self.current_streak = 0 # Current streak counter
        self.longest_streak = 0 # Longest streak counter

    def habit_name(self):
        """Prompts the user to name their new habit and confirm it."""
        while True:
            print("What new habit do you want to register?:")
            self.name = input().title()

            # Fail-safe for mistyping
            print(f"You entered '{self.name.title()}'. Is this correct? (yes/no):")
            name_confirmation = input().lower()

            if name_confirmation == "yes":
                break
            elif name_confirmation == "no":
                print("Let's try again!")

    def habit_frequency(self):
        """Prompts the user to assign their habit's frequency."""
        while True:
            print("Please type in 'Daily' or 'Weekly' to assign your habit's frequency:")
            new_habit_frequency = input().lower()

            if new_habit_frequency in ["daily", "weekly"]:
                self.frequency = new_habit_frequency
                break
            else:   # Deals with incorrect input
                print("Please enter either 'Daily' or 'Weekly'!")

    def creation_date(self):
        """Sets the creation date of the habit to the current date."""
        self.creation = datetime.now().date()