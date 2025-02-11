def _is_streak_broken(self, frequency, completions):
    """
    Check if streak is broken based on frequency.
    :param frequency: "str" daily or weekly habit
    :param completions: [list] of completion dates
    """
    sorted_completions = self._sort_completions(completions)

    if len(sorted_completions) < 2:
        return False  # Not enough completions to break a streak

    last_completion = sorted_completions[-2]
    current_completion = sorted_completions[-1]
    days_between = (current_completion - last_completion).days

    if frequency == "daily":
        return days_between > 1
    elif frequency == "weekly":
        return days_between > 7

