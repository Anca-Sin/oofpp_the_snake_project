from typing import List, Tuple

from .user import User
from .habit import Habit

class Analytics:
    """
    Algorithms using functional programming techniques which analyze a user's habit data.
    Spans across different dimensions including: streaks, completions and periodicity.
    Doesn't modify any existing data.

    Note: Most of the methods don't need to check for no habits/completions logic,
          because it is dealt with in the cli menus logic and db operations.

    Attributes:
        user: Reference to the User object whose habits will be analyzed.
              It is injected through the constructor, making the Analytics instance specific to its user.
    """

    def __init__(self, user: User) -> None:
        """
        Initializes the Analytics instance based on the provided user's data.

        Args:
            user: Central identity for all analytics operations.
        """
        self.user = user # Storing the user reference for analytics operations

    # Task requirement: "return a list of all currently tracked habits"
    def list_all_habits(self) -> List[Habit]:
        """
        Retrieves all the user's habits.

        Returns:
            A list of all Habit objects sorted alphabetically by name.
        """
        # Using list comprehension
        # return self.user.habits

        # Using FPP
        # Map extracts the identity of each habit from self.user.habits and returns the result as a sorted list
        all_habits_list = sorted(
            list(map(lambda habit: habit, self.user.habits)),
            key=lambda habit: habit.name
        )
        return all_habits_list

    # Task requirement: "return a list of all habits with the same periodicity"
    def list_habits_by_periodicity(self, periodicity: str) -> List[Habit]:
        """
        Retrieves the user's habits filtered by a given periodicity.

        Args:
            periodicity: The frequency to filter habits by ("daily" or "weekly).
        Returns:
            A list of Habit objects matching the given periodicity, sorted alphabetically by name.
        """
        # Using list comprehension
        # return [habit.name for habit in self.user.habits if habit.frequency == periodicity]

        # Using FPP
        # Filter habits to include only those with the given periodicity and return the matching habits as a list
        filtered_habits = sorted(
            list(filter(lambda habit: habit.frequency == periodicity, self.user.habits)),
            key=lambda habit: habit.name
        )
        return filtered_habits

    # Task requirement: "return the longest streak of all defined habits"
    def longest_streak_all_habits(self) -> Tuple[str, int]:
        """
        Finds the habit with the longest streak across all habits.

        Returns:
            A tuple containing (habit_name, longest_streak).
        """
        # Map each habit to a tuple of (name, longest_streak)
        # Then use max() to find the tuple with the highest longest_streak value
        longest_streak_all_habits = max(
            map(lambda habit: (habit.name, habit.streaks.get_longest_streak()), self.user.habits),
            key=lambda x: x[1] # Max counts the 2nd element
        )

        return longest_streak_all_habits[0], longest_streak_all_habits[1]

    # Task requirement: "return the longest streak for a given habit"
    def longest_streak_for_habit(self, habit_name: str) -> int:
        """
        Finds the longest streak for a selected habit.

        Args:
            habit_name: The name of the habit to get the longest streak for.
        Returns:
            The longest streak for the selected habit.
        """
        # Direct look-up with next() since habit names are unique
        habit = next((h for h in self.user.habits if h.name == habit_name), None)

        return habit.streaks.get_longest_streak() if habit else 0

    def longest_streak_by_periodicity(self, periodicity: str) -> Tuple[str, int]:
        """
        Finds the habit with the longest streak for a given periodicity.

        Args:
            periodicity: The periodicity to filter by ("daily" or "weekly").
        Returns:
            A tuple of (habit_name, longest_streak)
                    or ("None", 0) if no habit exists; not accounted for in the cli logic.
        """
        # Filter habits by periodicity
        habits = self.list_habits_by_periodicity(periodicity)

        # Check if no habits exist with chosen periodicity
        # E.g.: user might have daily habits but no weekly yet
        if not habits:
            return "None", 0

        # Find the habit with the maximum longest_streak
        max_habit = max(habits, key=lambda h: h.streaks.longest_streak) # Max counts the longest_streak value
        return max_habit.name, max_habit.streaks.longest_streak

    def most_completed_habit(self) -> Tuple[str, int]:
        """
        Finds the habits with the most completions across all habit.

        Returns:
             A tuple of (habit_name, completion_count).
        """
        # Map each habit to a tuple of (name, completion_count)
        # Then find the tuple with the highest count
        most_completed = max(
            map(lambda habit: (habit.name, len(habit.completion_dates)), self.user.habits),
            key=lambda x: x[1] # Max counts the 2nd element (completion count)
        )

        return most_completed

    def most_completed_by_periodicity(self, periodicity: str) -> Tuple[str, int]:
        """
        Finds the habit with the most completions for a given periodicity.

        Args:
            periodicity: The periodicity to filter by ("daily" or "weekly")
        Returns:
            A tuple of (habit_name, completion_count)
                    or ("None", 0) if no habit exists; not accounted for in the cli logic.
        """
        # Filter habits by periodicity
        habits = self.list_habits_by_periodicity(periodicity)

        # Check if no habit exists with chosen periodicity
        if not habits:
            return "None", 0

        # Find the habit with the max number of completions
        max_habit = max(habits, key=lambda h: len(h.completion_dates)) # Max counts the nr. of completions
        return max_habit.name, len(max_habit.completion_dates)

    def least_completed_habit(self) -> tuple:
        """
        Finds the habit with the fewest completions across all habits.

        Returns:
            A tuple of (habit_name, completion_count).
        """
        # Map each habit to a tuple of (name, completion_count)
        # Then find the tuple with the lowest count
        least_completed = min(
            map(lambda habit: (habit.name, len(habit.completion_dates)), self.user.habits),
            key=lambda x: x[1] # Min counts the 2nd element (completion_count)
        )

        return least_completed

    def least_completed_by_periodicity(self, periodicity: str) -> Tuple[str, int]:
        """
        Finds the habit with the fewest completions for a given periodicity.

        Args:
            periodicity: The periodicity to filter by ("daily" or "weekly).
        Returns:
             A tuple of (habit_name, completion_count)
                     or ("None", 0) if no habit exists; not accounted for in the cli logic.
        """
        # Filter habits by periodicity
        habits = self.list_habits_by_periodicity(periodicity)

        # Check if no habit exists with chosen periodicity
        if not habits:
            return "None", 0

        # Find the habit with the minimum number of completions
        min_habit = min(habits, key=lambda h: len(h.completion_dates)) # Min counts the nr. of completions
        return min_habit.name, len(min_habit.completion_dates)

    def average_streak_length_habit(self, habit_name: str) -> float:
        """
        Calculates the average streak length for a selected habit.

        Args:
            habit_name: The name of the habit to analyze.
        Returns:
            The average streak of a habit as a float.
        """
        streaks = []

        # Find the selected habit
        target_habit = next(habit for habit in self.user.habits if habit.name == habit_name)

        # Add current streak if positive
        if target_habit.streaks.current_streak > 0:
                streaks.append(target_habit.streaks.current_streak)

        # Add all broken streak lengths directly from the habit object
        streaks.extend(target_habit.streaks.broken_streak_lengths)

        # Calculate the average (handling empty list)
        return sum(streaks) / len(streaks) if streaks else 0

    def average_streak_all_habits(self) -> float:
        """
        Calculates the average streak length across all habits.

        Returns:
            The average streak across all habits as a float.
        """
        # Initialize an empty list to collect streak lengths from all habits
        all_streak_lengths = []

        # Add current streak if positive
        for habit in self.user.habits:
            if habit.streaks.current_streak > 0:
                all_streak_lengths.append(habit.streaks.current_streak)

            # Add all broken streak lengths directly
            all_streak_lengths.extend(habit.streaks.broken_streak_lengths)

        # Calculate the average (handling empty list)
        return sum(all_streak_lengths) / len(all_streak_lengths) if all_streak_lengths else 0

    def average_streak_by_periodicity(self, periodicity: str) -> float:
        """
        Calculates the average streak length for habits with a given periodicity.

        Args:
            periodicity: The periodicity to filter by ("daily" or "weekly")
        Returns:
            The average streak length across daily and weekly habits as a float.
        """
        # Initialize an empty list to collect streak lengths
        all_streak_lengths = []

        # Filter habits by periodicity
        habits = self.list_habits_by_periodicity(periodicity)

        # Process each habit to collect streak lengths
        for habit in habits:
            # Add current streak if positive
            if habit.streaks.current_streak > 0:
                # Add it to all_streak_lengths
                all_streak_lengths.append(habit.streaks.current_streak)

            # Add all broken streak lengths directly
            all_streak_lengths.extend(habit.streaks.broken_streak_lengths)

        # Calculate the average (handling the case of empty list)
        return sum(all_streak_lengths) / len(all_streak_lengths) if all_streak_lengths else 0