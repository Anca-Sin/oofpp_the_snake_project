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