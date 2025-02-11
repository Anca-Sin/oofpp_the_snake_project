


def _is_streak_broken(self, frequency, completions):
    """
    Check if streak is broken based on frequency.
    :param frequency: "str" daily or weekly habit
    :param completions: [list] of completion dates
    """
    # Sort completions by date, in perspective of allowing users to add past completion dates
    sorted_completions = sorted(completions)
    last_completion = sorted_completions[-2]
    current_completion = sorted_completions[-1]
    days_between = (current_completion - last_completion).days

def calculate_current_streak(self, frequency, completions):
    """
    Calculates current streak based on habit frequency and completion dates.
    :param frequency: (str) "daily" or "weekly"
    :param completions: (list) of completion dates
    """
    if len(completions) == 0:
        return self.current

    # Sort completions by date, in perspective of allowing users to add past completion dates
    sorted_completions = sorted(completions)

    if frequency == "daily":
        # Check for consecutive days in a row, count them and return the streak
        # dont i need to add also something in frequency in habit.py?