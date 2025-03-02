from db_and_managers.database import Database

from datetime import datetime, timedelta, date
from typing import List

# Class Design:
# - Handles streak calculations for individual habits
# - Low-level calculations for determining if a streak is broken
# - Maintains state (current_streak and longest_streak)
# - Ties directly to individual habit instances (each habit has its own Streaks object)

class Streaks:
    """Tracks current and longest streaks with basic functionality for now."""

    def __init__(self, db: Database = None):
        self.current_streak: int = 0 # Current streak counter
        self.longest_streak: int = 0 # Longest streak counter
        self.db = db                 # Initialize a db instance

    @staticmethod
    def _sort_completions(completions: List[date]) -> List[date]:
        """
        Sorts completion dates externally to be used across all methods.

        :param completions: List of completion dates.
        :return: Sorted list of completion dates.
        """
        return sorted(completions)

    @staticmethod
    def _is_streak_broken(frequency: str, latest_completion: date, habit_id: int) -> bool:
        """
        Helper method to reset streak counter to 0 if streak is broken.

        :param frequency: The frequency of the habit ("daily" or "weekly").
        :param latest_completion: The date of the latest completion.
        :param habit_id: The ID of the habit whose streak was broken.
        :return: True if streak is broken, False otherwise.
        """
        today = datetime.now().date()

        if frequency == "daily" and (today - latest_completion).days > 1:
            # Save broken streak length to the db before resetting
            self.db.save_broken_streak_length(habit_id, self.current_streak)
            return True
        elif frequency == "weekly" and (today - latest_completion).days > 7:
            self.db.save_broken_streak_length(habit_id, self.current_streak)
            return True

        return False

    def get_current_streak(self, frequency: str, completions: List[date]) -> int:
        """
        Calculates current streak based on habit frequency and completion dates.

        :param frequency: The frequency of the habit ("daily" or "weekly").
        :param completions: List of completion dates
        :return: The current streak count
        """
        if len(completions) == 0:
            return self.current_streak

        sorted_completions = self._sort_completions(completions)

        # Check if streak is broken by passing frequency and latest completion date,
        # and if broken, immediately exit.
        if self._is_streak_broken(frequency, sorted_completions[-1]):
            return self.current_streak

        # If no streak was broken start with first completion
        self.current_streak = 1

        # Compare consecutive dates
        # Iterate backwards to compare each date with the previous date
        for i in range(len(sorted_completions)-1, 0, -1):
            current_date = sorted_completions[i]
            previous_date = sorted_completions[i - 1]

            if frequency == "daily":
                # Check if dates are consecutive
                if (current_date - previous_date).days == 1:
                    self.current_streak += 1
                else:
                    break # Streak is broken

            elif frequency == "weekly":
                # Find days since Monday
                days_since_monday = current_date.weekday()
                days_since_last_monday = previous_date.weekday()

                # Get the Monday of current_date's week
                current_monday = current_date - timedelta(days=days_since_monday)
                previous_monday = previous_date - timedelta(days=days_since_last_monday)

                # Check if Mondays are one week apart
                if (current_monday - previous_monday).days == 7:
                    self.current_streak += 1
                else:
                    break # Streak is broken

        # Longest streak needs to be updated each time we calculate a current streak
        self.longest_streak = max(self.longest_streak, self.current_streak)

        return self.current_streak

    def get_longest_streak(self) -> int:
        """
        Gets the longest streak achieved for this habit.

        :return: The longest streak as an integer.
        """
        return self.longest_streak