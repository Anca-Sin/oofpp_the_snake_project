from .user import User
from .habit import Habit
from .streaks import Streaks

class DataAnalytics:
    """Analyzes the user's habits and provide statistics."""

    def __init__(self, user: User) -> None:
        """
        Initializes the DataAnalytics object.

        :param user: The User object whose habits will be analyzed.
        """
        self.user = user         # Store the user for analytics
        self.streaks = Streaks() # Create an instance of Streaks to analyze