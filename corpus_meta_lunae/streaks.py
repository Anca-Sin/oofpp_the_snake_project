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

    def _is_streak_broken(self, frequency, latest_completion):
        """Helper method to reset streak counter to 0 if streak is broken."""
        today = datetime.now().date()

        if frequency == "daily" and (today - latest_completion).days > 1:
            return True
        elif frequency == "weekly" and (today - latest_completion).days > 7:
            return True

        return False    # Streak is not broken

    def calculate_current_streak(self, frequency, completions):
        """
        Calculates current streak based on habit frequency and completion dates.
        :param frequency: (str) "daily" or "weekly"
        """
        if len(completions) == 0:
            return self.current

        sorted_completions = self._sort_completions(completions)

        # Check if streak is broken by passing frequency and latest completion date,
        # and if broken, immediately exit.
        if self._is_streak_broken(frequency, sorted_completions[-1]):
            return self.current

        # If no streak was broken start with first completion
        self.current = 1

        # Compare consecutive dates
        # Iterate backwards to compare each date with the previous date
        for i in range(len(sorted_completions)-1, 0, -1):
            current_date = sorted_completions[i]
            previous_date = sorted_completions[i - 1]

            if frequency == "daily":
                # Check if dates are consecutive
                if (current_date - previous_date).days == 1:
                    self.current += 1
                else:
                    break   # Streak is broken

            elif frequency == "weekly":
                # Find days since Monday
                days_since_monday = current_date.weekday()
                days_since_last_monday = previous_date.weekday()

                # Get the Mondat of current_date's week
                current_monday = current_date - timedelta(days=days_since_monday)
                previous_monday = previous_date - timedelta(days=days_since_last_monday)

                # Check if Mondays are one week apart
                if (current_monday - previous_monday).days == 7:
                    self.current += 1
                else:
                    break   # Streak is broken

        self.longest = max(self.longest, self.current)
        return self.current

    def get_longest_streak(self):
        """Returns the longest streak achieved for this habit."""
        return self.longest
