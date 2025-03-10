from datetime import datetime, timedelta, date
from typing import List

class Streaks:
    """
    Tracks and calculates streak information for habits.

    - handles the logic for determining current and longest streaks, and keeping a history of broken streaks
    - provides methods to check if a streak is broken and to calculate streak lengths based on habit completion dates

    Attributes:
        current_streak (int): The current active streak count.
        longest_streak (int): The longest streak achieved.
        broken_streak_length (List[int]): History of streak lengths when they were broken.
    """

    def __init__(self):
        """Initializes a new Streak object with default values."""
        self.current_streak: int = 0               # Current streak counter
        self.longest_streak: int = 0               # Longest streak counter
        self.broken_streak_length: List[int] = []  # History of broken streak lengths

    @staticmethod
    def _sort_completions(completions: List[date]) -> List[date]:
        """
        Sorts completion dates externally to be used across all methods.

        - ensures dates are processed in the correct order when calculating streaks

        Returns:
            A sorted list of completion dates.
        """
        return sorted(completions) # Returns dates in ascending order

    def is_streak_broken(self, frequency: str, latest_completion: date) -> bool:
        """
        Determines if a streak is broken based on the frequency and latest completion date.

        - checks if there are any completions
        - checks if the streak is broken
        - if yes, it adds the current streak length to the broken_streak_length history
        - then resets the current_streak to 0

        Args:
            frequency: The frequency of the habit ("daily" or "weekly").
            latest_completion: The date of the most recent completion.
                                      Retrieved in get_current_streak() where is_streak_broken is called.

        Returns:
            True if streak is broken, False if still active streak.
        """
        today = datetime.now().date()

        # For daily habits, streak is broken if more than 1 day has passed since last completion
        if frequency == "daily" and (today - latest_completion).days > 1:
            # Save broken streak length to the list
            self.broken_streak_length.append(self.current_streak)
            # Reset current streak
            # Only today's completion
            self.current_streak = 1
            return True

        # For weekly habits
        elif frequency == "weekly":
            # Calculate the Monday of the current week (weekday() returns 0 for Monday)
            current_week_monday = today - timedelta(days=today.weekday())

            # Calculate the Monday of the week of the last completion
            last_completion_week_monday = latest_completion - timedelta(days=latest_completion.weekday())

            # Streak is broken if current week's Monday is more than 7 days apart from the latest completion's Monday
            if current_week_monday > last_completion_week_monday + timedelta(days=7):
                # Save broken streak length to the list
                self.broken_streak_length.append(self.current_streak)
                # Reset current streak
                # Only today's completion
                self.current_streak = 1
                return True

        return False

    def get_current_streak(self, frequency: str, completions: List[date]) -> int:
        """
        Calculates the current streak of the selected habit based on habit frequency and completion dates.

        - checks if there are any completions
        - checks if the streak is broken
        - updates the current streak count
        - updates the longest streak if needed

        Args:
            frequency: The frequency of the habit ("daily" or "weekly").
            completions: List of dates when the habit was completed.
        Returns:
            The current streak count.
        """
        # If no completions, current streak is 0
        if not completions:
            self.current_streak = 0
            return self.current_streak

        # Sort completions to process them chronologically
        sorted_completions = self._sort_completions(completions)
        # Get latest completion
        latest_completion = sorted_completions[-1]

        # Check if streak is broken (using most recent completion)
        if self.is_streak_broken(frequency, latest_completion):
            # If streak is broken, current_streak was already reset in is_streak_broken()
            return self.current_streak

        # If streak isn't broken
        # Start with at least 1 since we passed 0 completions check
        self.current_streak = 1

        if frequency == "daily":
            # Iterate backwards
            #   starting with last index
            #   stopping before the first index
            #   with a step of -1
            for i in range(len(sorted_completions) - 1, 0, -1):
                # [i-1] will now compare also the first completion on the list
                # Check if completions are 1 day apart
                if (sorted_completions[i] - sorted_completions[i-1]).days == 1:
                    # Increment count by 1 for each consecutive days
                    self.current_streak += 1
                else:
                    break # Current streak goes back to 1

        elif frequency == "weekly":
            # Get the Monday of the most recent completion
            latest_monday = latest_completion - timedelta(days=latest_completion.weekday())

            # Iterate backwards through completions to count consecutive weeks
            for i in range(len(sorted_completions) - 1, 0, -1):
                # Get Mondays for consecutive completions
                current_monday = sorted_completions[i] - timedelta(days=sorted_completions[i].weekday())
                previous_monday = sorted_completions[i-1] - timedelta(days=sorted_completions[i-1].weekday())

                # Check if completions are 1 week apart
                if (current_monday - previous_monday).days == 7:
                    self.current_streak += 1
                else:
                    break

        # Update the longest streak if current streak is longer
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak

        return self.current_streak

    def get_longest_streak(self) -> int:
        """
        Gets the longest streak achieved for the selected habit.

        Returns:
            The longest streak count.
        """
        return self.longest_streak