from datetime import datetime, timedelta

class Streaks:
    """Tracks current and longest streaks with basic functionality for now."""
    def __init__(self):
        self.current = 0 # Current streak counter
        self.longest = 0 # Longest streak counter
        # self.announce_streaks ? does the user request a specific streak or display all?

    def _sort_completions(self, completions):
        """
        Sorting completion dates externally to be used across all methods.
        :param completions: (list) of completion dates
        """
        return sorted(completions)

    def calculate_current_streak(self, frequency, completions):
        """
        Calculates current streak based on habit frequency and completion dates.
        :param frequency: (str) "daily" or "weekly"
        """
        if len(completions) == 0:
            return self.current

        sorted_completions = self._sort_completions(completions)
        streak = 1 # Start with first completion

        # Compare consecutive dates
        # Iterate backwards to compare each date with the previous date
        for i in range(len(sorted_completions)-1, 0, -1):
            current_date = sorted_completions[i]
            previous_date = sorted_completions[i - 1]

            if frequency == "daily":
                # Check if dates are consecutive
                if (current_date - previous_date).days == 1:
                    streak += 1
                else:
                    break

            elif frequency == "weekly":
                if (current_date - previous_date).days == 7:
                    streak += 1
                else:
                    break

        self.current = streak
        return self.current

