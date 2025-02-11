from datetime import datetime, timedelta

class Streaks:
    """Tracks current and longest streaks with basic functionality for now."""
    def __init__(self):
        self.current = 0 # Current streak counter
        self.longest = 0 # Longest streak counter
        # self.announce_streaks ? does the user request a specific streak or display all?

    def _sort_completions(self, completions):
        """Sorting completion dates externally to be used across all methods."""
        return sorted(completions)
