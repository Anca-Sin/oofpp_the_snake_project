from .user import User
from .habit import Habit
from .streaks import Streaks

# "The functionality of this analytics module must be implemented using the functional programming paradigm."
class Analytics:
    """Analyzes the user's habits and provide statistics."""

    def __init__(self, user: User) -> None:
        """
        Initializes the DataAnalytics object.

        :param user: The User object whose habits will be analyzed.
        """
        self.user = user         # Store the user for analytics
        self.streaks = Streaks() # Create an instance of Streaks to analyze

    # Task requirement: "return a list of all currently tracked habits"
    def list_all_habits(self):

    # Task requirement: "return a list of all habits with the same periodicity"

    # Task requirement: "return the longest streak of all defined habits"

    # Task requirement: "return the longest streak for a given habit"