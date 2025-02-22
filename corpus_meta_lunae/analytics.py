from .user import User
from .habit import Habit
from .streaks import Streaks
from typing import List

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
    def list_all_habits(self) -> List[str]:
        """
        Retrieves the current habits of the user.

        :return: List of habit names.
        """
        # Using list comprehension
        # return [habit.name for habit in self.user.habits]

        # Using FPP
        # Map extracts the "name" of each habit from self.user.habits and returns the result as a list
        all_habits_list = list(map(lambda habit: habit.name, self.user.habits))
        print(f"{self.user.username.title()}'s current habit list: {', '.join(all_habits_list).title()}")
        return all_habits_list

    # Task requirement: "return a list of all habits with the same periodicity"
    def list_habits_by_periodicity(self, periodicity: str) -> List[str]:
        """
        Retrieves habits filtered by the period of their completion (daily or weekly).

        :param periodicity: The frequency to filter habits by.
        :return: List of habit names that match the given filter.
        """
        # Using list comprehension
        # return [habit.name for habit in self.user.habits if habit.frequency == periodicity]

        # Using FPP
        # Filter habits to include only those with the given periodicity and return the matching habits as a list
        filtered_habits_list = list(filter(lambda habit: habit.frequency == periodicity, self.user.habits))
        print(f"{self.user.username.title()}'s current {periodicity} habits: {', '.join(filtered_habits_list).title()}")
        return filtered_habits_list

    # Task requirement: "return the longest streak of all defined habits"

    # Task requirement: "return the longest streak for a given habit"