from datetime import datetime, timedelta, date
from typing import List

# Class Design:
# - Handles streak calculations for individual habits
# - Low-level calculations for determining if a streak is broken
# - Maintains state (current_streak and longest_streak)
# - Ties directly to individual habit instances (each habit has its own Streaks object)

class Streaks:
    """Tracks current and longest streaks with basic functionality for now."""

    def __init__(self):
        self.current_streak: int = 0               # Current streak counter
        self.longest_streak: int = 0               # Longest streak counter
        self.broken_streak_length: List[int] = []  # A broken streak's length

    @staticmethod
    def _sort_completions(completions: List[date]) -> List[date]:
        """
        Sorts completion dates externally to be used across all methods.

        :param completions: List of completion dates.
        :return: Sorted list of completion dates.
        """
        return sorted(completions)

    def is_streak_broken(self, frequency: str, latest_completion: date) -> bool:
        """
        Method to update the broken streaks list and reset streak counter to 0 if streak is broken.

        :param frequency: The frequency of the habit ("daily" or "weekly").
        :param latest_completion: The date of the latest completion.
        :return: True if streak is broken, False otherwise.
        """
        today = datetime.now().date()

        if frequency == "daily" and (today - latest_completion).days > 1:
            # Save broken streak length to the list
            self.broken_streak_length.append(self.current_streak)
            self.current_streak = 0
            return True
        elif frequency == "weekly" and (today - latest_completion).days > 7:
            self.broken_streak_length.append(self.current_streak)
            self.current_streak = 0
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

        # Check if streak is broken
        if self.current_streak > 0 and self.is_streak_broken(frequency, sorted_completions[-1]):
            self.current_streak = 0
            return self.current_streak

        # If no streak was broken
        self.current_streak += 1

        # Longest streak needs to be updated each time we calculate a current streak
        self.longest_streak = max(self.longest_streak, self.current_streak)

        return self.current_streak

    def get_longest_streak(self) -> int:
        """
        Gets the longest streak achieved for this habit.

        :return: The longest streak as an integer.
        """
        return self.longest_streak