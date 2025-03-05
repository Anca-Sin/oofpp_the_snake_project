from .user import User
from .habit import Habit
from typing import List

# Task requirement:
# "The functionality of this analytics module must be implemented using the functional programming paradigm."

# Class Design:
# - Provides broad, higher-level calculations across multiple habits
# - Doesn't maintain state of its own, but analyzes user/habit data
# - Already uses Streaks functionality through habit.streaks references

class Analytics:
    """Analyzes the user's habits and provide statistics."""

    def __init__(self, user: User) -> None:
        """
        Initializes the DataAnalytics object.

        :param user: The User object whose habits will be analyzed.
        """
        self.user = user         # Store the user for analytics

    # Task requirement: "return a list of all currently tracked habits"
    def list_all_habits(self) -> List[Habit]:
        """
        Retrieves the current habits of the user.

        :return: List of habit names.
        """
        # Using list comprehension
        # return self.user.habits

        # Using FPP
        # Map extracts the "name" of each habit from self.user.habits and returns the result as a list
        all_habits_list = list(map(lambda habit: habit, self.user.habits))
        return all_habits_list

    # Task requirement: "return a list of all habits with the same periodicity"
    def list_habits_by_periodicity(self, periodicity: str) -> List[Habit]:
        """
        Retrieves habits filtered by the period of their completion (daily or weekly).

        :param periodicity: The frequency to filter habits by.
        :return: List of habit names that match the given filter.
        """
        # Using list comprehension
        # return [habit.name for habit in self.user.habits if habit.frequency == periodicity]

        # Using FPP
        # Filter habits to include only those with the given periodicity and return the matching habits as a list
        filtered_habits = list(filter(lambda habit: habit.frequency == periodicity, self.user.habits))
        return filtered_habits

    # Task requirement: "return the longest streak of all defined habits"
    def longest_streak_all_habits(self) -> tuple:
        """
        Retrieves the longest streak of all defined habits.

        :return: A tuple (habit_name, longest_streak) of the habit with the longest streak.
        """
        # Using FPP
        # map() to iterate through the longest streak for each habit and compare the streaks (second element)
        #   and use max() to get the highest value

        # Don't need to check no habits logic
        # It is dealt with in the menu_analytics_all_habits()
        longest_streak_all_habits = max(
            map(lambda habit: (habit.name, habit.streaks.get_longest_streak()), self.user.habits),
            key=lambda x: x[1]
        )

        return longest_streak_all_habits[0], longest_streak_all_habits[1]

    # Task requirement: "return the longest streak for a given habit"
    def longest_streak_for_habit(self, habit_name: str) -> tuple:
        """
        Retrieves the longest streak for a given habit.

        :param habit_name: The name of the habit to get the longest streak for.
        :return: A tuple (habit_name, longest_streak) of the longest streak for a selected habit.
        """
        # Using FPP
        # Use next() to get the first matching habit (or None if no match),
        #   while iterating with filter() over self.user.habits applying the lambda function
        habit = next(
            filter(lambda habit_item: habit_item.name == habit_name, self.user.habits),
            None
        )

        return habit_name, habit.streaks.get_longest_streak()

    def longest_streak_by_periodicity(self, periodicity: str) -> tuple:
        """
        Returns the habit with the longest streak for a specific periodicity.

        :param periodicity: The periodicity to filter by ("daily" or "weekly").
        :return: Tuple of (habit_name, longest_streak) or ("None", 0) if no habits.
        """
        # Filter habits by periodicity
        habits = self.list_habits_by_periodicity(periodicity)

        # Check if no habits exist with chosen periodicity
        if not habits:
            return "None", 0

        # Else return the tuple with habit_name, longest_streak
        max_habit = max(habits, key=lambda h: h.streaks.longest_streak)
        return max_habit.name, max_habit.streaks.longest_streak

    def most_completed_habit(self) -> tuple:
        """
        Finds the habits with the most completions.

        :return: A tuple (habit_name, completion_count) of the habit
        """
        # Passing max() to the list of tuples created by iterating with map()
        #   to find the tuple with the highest count of completions

        most_completed = max(
            map(lambda habit: (habit.name, len(habit.completion_dates)), self.user.habits),
            key=lambda x: x[1] # Sort by completion count
        )

        return most_completed

    def most_completed_by_periodicity(self, periodicity: str) -> tuple:
        """
        Returns the habit with the most completions for a specific periodicity.

        :param periodicity: The periodicity to filter by ("daily" or "weekly).
        :return: Tuple of (habit_name, completion_count) or ("None", 0) if no habits.
        """
        # Filter habits by periodicity
        habits = self.list_habits_by_periodicity(periodicity)

        if not habits:
            return "None", 0

        max_habit = max(habits, key=lambda h: len(h.completion_dates))
        return max_habit.name, len(max_habit.completion_dates)

    def least_completed_habit(self) -> tuple:
        """
        Finds the habit with the fewest completions.

        :return: A tuple (habit_name, completion_count) of the habit
        """
        # Passing min() to the list of tuples created by iterating with map()
        #   to find the tuple with the lowest count of completions
        least_completed = min(
            map(lambda habit: (habit.name, len(habit.completion_dates)), self.user.habits),
            key=lambda x: x[1]
        )

        return least_completed


    def least_completed_by_periodicity(self, periodicity: str) -> tuple:
        """
        Returns the habit with the most completions for a specific periodicity.

        :param periodicity: The periodicity to filter by ("daily" or "weekly).
        :return: Tuple of (habit_name, completion_count) or ("None", 0) if no habits.
        """
        # Filter habits by periodicity
        habits = self.list_habits_by_periodicity(periodicity)

        if not habits:
            return "None", 0

        min_habit = min(habits, key=lambda h: len(h.completion_dates))
        return min_habit.name, len(min_habit.completion_dates)

    def average_streak_length_habit(self, habit_name: str) -> float:
        """
        Calculates the average streak length for a given habit based on its recorded streak length history.

        :param habit_name: The name of the habit to analyze.
        :return: The average streak length as a float.
        """
        # Don't need to check no habit logic
        # Only Habit Details Menu uses this method: no habit = no menu

        # Get the streak length history string from the db
        # Returns a comma separated string of string lengths
        streak_history = self.user.db.load_broken_streak_length(habit_name)

        # If no history exists
        if not streak_history:
            return 0.0

        # Convert the comma separated string into a list of integers
        # map() applies int() to each element of the split string
        # list() converts the map object to a list for further processing
        streak_lengths = list(map(int, streak_history.split(",")))

        # Calculate the average
        average_streak = sum(streak_lengths) / len(streak_lengths)

        return average_streak

    def average_streak_all_habits(self) -> float:
        """
        Calculates the average streak length across all habits.

        :return: Average streak as a float.
        """
        # Don't need to check no habits logic
        # It is dealt with in the menu_analytics_all_habits()

        # Initialize an empty list to collect streak lengths from all habits
        all_streak_lengths = []

        # Iterate through all habits for the current user
        for habit in self.user.habits:
            # Retrieve streak history for each habit
            streak_history = self.user.db.load_broken_streak_length(habit.name)

            # If streak history exists, convert and add to the collection
            if streak_history:
                all_streak_lengths.extend(list(map(int, streak_history.split(","))))

        # Calculate the average
        average_streak = sum(all_streak_lengths) / len(all_streak_lengths) if all_streak_lengths else 0.0

        return average_streak

    def average_streak_by_periodicity(self, periodicity: str) -> float:
        """
        Calculates the average streak length for a specific periodicity based on streak history.

        :param periodicity: The periodicity to filter by ("daily" or "weekly")
        :return: Average streak as a float.
        """
        # Filter habits by periodicity
        habits = self.list_habits_by_periodicity(periodicity)

        # Initialize an empty list to collect streak lengths
        all_streak_lengths = []

        # Iterate through habits with the specified periodicity
        for habit in habits:
            streak_history = self.user.db.load_broken_streak_length(habit.name)

            # If streak history exists, convert and add to collection
            if streak_history:
                all_streak_lengths.extend(list(map(int, streak_history.split(","))))

        # Calculate the average
        average_streak = sum(all_streak_lengths) / len(all_streak_lengths) if all_streak_lengths else 0.0

        return average_streak