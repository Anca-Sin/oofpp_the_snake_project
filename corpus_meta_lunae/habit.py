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
        self.custom_frequency = None    # Holds the user-input custom frequency range
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
            print("Please type in 'Daily', 'Weekly', or 'Custom' to assign your habit's frequency:")
            self.frequency = input().lower()

            # Handle custom frequency
            if self.frequency == "custom":
                self.set_custom_frequency() # Call the custom frequency setup method

            # Handle pre-defined daily and weekly frequencies
            elif self.frequency in ["daily", "weekly"]:
                self.frequency = confirm_input("frequency", self.frequency)

            # Handle miss-spelling
            else:
                print("Invalid Input. Pleas enter 'Daily', 'Weekly', or 'Custom'!")

    def set_custom_frequency(self):
        """
        Prompts the user to input a desired custom frequency:
        either a single value or a range (e.g., '3' or '3-4' times a week).
            """
        while True:
            print("""Please specify your desired custom frequency as, for example:
- '3', for a single weekly value to track
or
- '3-5', times a week as a range for your tracked habit""")
            custom_input = input().strip() # Take input and remove any surrounding whitespaces

            # Handle a single value input for custom frequency
            if custom_input.isdigit(): # If the input is a single number
                times_per_week = int(custom_input)
                self.custom_frequency = (times_per_week, times_per_week) # Set both min and max to the same value
                self.frequency = "custom" # Set the frequency type to custom
                # Use confirm_input helper function to confirm custom frequency
                self.custom_frequency = confirm_input("frequency", f"{times_per_week} times a week")
                break

            # Handle a range input for custom frequency
            # Allowing the user to insert any range is intended (exceeding 7 times/week)
            elif "-" in custom_input: # If it contains a dash, indicate a range
                try:
                    # Try to split the input by the dash into two integers
                    min_freq, max_freq = map(int, custom_input.split("-"))

                    if min_freq < max_freq: # Ensure min is less than max
                        self.custom_frequency = (min_freq, max_freq) # Store the range as a tuple
                        self.frequency = "custom" # Set the frequency type to custom
                        # Use confirm_input helper function to confirm custom frequency
                        self.custom_frequency = confirm_input("frequency", f"{min_freq}-{max_freq} times a week")
                        break

                    else:
                        print("The minimum frequency must be lower than the maximum frequency, or enter a single value!")
                except ValueError:
                    print("Invalid Format. Please enter a valid range, like '3-5', or a single digit.")

            else:
                # If the input doesn't match either format, prompt the user again
                print("Invalid Input. Please enter a single value (e.g. '3') or a range (e.g. '3-5')")

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

        elif self.frequency == "custom":
            # Handle it like daily and weekly but with custom range
            if self.custom_frequency:
                min_freq, max_freq = self.custom_frequency  # min and max completions for custom frequency
                # Calculate the start of the current week (Monday)
                week_start = current_date - timedelta(days=current_date.weekday())
                week_completions = [date for date in self.completions if date >= week_start.date()]

                # Check if the number of completions isn't fully completed
                if len(week_completions) < max_freq:
                    self.completions.append(current_date.date())
                    print(f"'{self.name.title()}' checked off successfully!")
                    self.streaks.calculate_current_streak(self.frequency, self.completions)
                    return True

                else:
                    print(f"'{self.name.title()}' has already been fully completed this week!")
                    return False