from .user import User
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

        # Extract habit names from the Habit object to avoid TypeError (expected str instance, Habit found)
        habit_names = list(map(lambda habit: habit.name, filtered_habits_list))
        print(f"{self.user.username.title()}'s current {periodicity} habits: {', '.join(habit_names).title()}")
        return habit_names

    # Task requirement: "return the longest streak of all defined habits"
    def longest_streak_all_habits(self) -> tuple:
        """
        Retrieves the longest streak of all defined habits.

        :return: A tuple (habit_name, longest_streak) of the habit with the longest streak.
        """
        # Using FPP
        # map() to iterate through the longest streak for each habit and compare the streaks (second element)
        #   and use max() to get the highest value
        longest_habit_all = max(
            map(lambda habit: (habit.name, habit.streaks.get_longest_streak()), self.user.habits),
            key=lambda x: x[1]
        )

        print(f"The habit with the longest streak is '{longest_habit_all[0].title()}', "
              f"with {longest_habit_all[1]} completions!")

        return longest_habit_all[0], longest_habit_all[1]

    # Task requirement: "return the longest streak for a given habit"
    def longest_streak_for_habit(self, habit_name: str) -> int:
        """
        Retrieves the longest streak for a given habit.

        :param habit_name: The name of the habit to get the longest streak for.
        :return: The longest streak for the specified habit.
        """
        # Using FPP
        # Use next() to get the first matching habit (or None if no match),
        #   while iterating with filter() over self.user.habits applying the lambda function
        habit = next(
            filter(lambda habit_item: habit_item.name == habit_name, self.user.habits),
            None
        )

        # If no match is found
        if habit is None:
            raise ValueError(f"Habit '{habit_name.title()}' not found!")

        print(f"The longest streak for '{habit_name.title()}' is: {habit.streaks.get_longest_streak()}!")
        return habit.streaks.get_longest_streak()
