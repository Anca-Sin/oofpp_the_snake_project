from datetime import datetime, timedelta, date
from typing import List


class Streaks:
    """
    Tracks and calculates streak information for habits.

    - handles the logic for determining current and longest streaks, and keeping a history of broken streaks
    - provides methods to check if a streak is broken and to calculate streak lengths based on habit completion dates

    Attributes:
        current_streak (int): The current active streak count.
        longest_streak (int): The longest streak achieved.
        broken_streak_lengths (List[int]): History of streak lengths when they were broken.
    """

    def __init__(self):
        """Initializes a new Streak object with default values."""
        self.current_streak: int = 0               # Current streak counter
        self.longest_streak: int = 0               # Longest streak counter
        self.broken_streak_lengths: List[int] = []  # History of broken streak lengths

    def is_streak_broken(self, frequency: str, completions: List[date]) -> bool:
        """
        Determines if a streak is broken based on the frequency and latest completion date.

        - checks if the streak is broken
        - if yes, it adds the current streak length to the broken_streak_lengths history
        - then resets the current_streak to 1

        Args:
            frequency: The frequency of the habit ("daily" or "weekly").
            completions: List of completion dates.
                         They are passed from the Habits object which owns the Streaks instance.
        Returns:
            True if streak is broken, False if still active streak.
        """
        today = datetime.now().date()

        sorted_completions = sorted(completions)
        last_completion = sorted_completions[-1]

        # For daily habits, streak is broken if more than 1 day has passed since last completion
        if frequency == "daily":
            if (today - last_completion).days > 1:
                # Save broken streak length to the list
                self.broken_streak_lengths.append(self.current_streak)
                # Reset current streak
                # Only today's completion
                self.current_streak = 1
                return True

        # Streak is broken if current week's Monday is more than 7 days apart from last_completion's Monday
        elif frequency == "weekly":
            # Calculate the Monday of the current week (weekday() returns 0 for Monday)
            current_week_monday = today - timedelta(days=today.weekday())

            # Calculate the Monday of the week of the last completion
            last_completion_week_monday = last_completion - timedelta(days=last_completion.weekday())

            # Streak is broken if current week's Monday is more than 7 days apart from the latest completion's Monday
            if current_week_monday > last_completion_week_monday + timedelta(days=7):
                # Save broken streak length to the list
                self.broken_streak_lengths.append(self.current_streak)
                # Reset current streak
                # Only today's completion
                self.current_streak = 1
                return True

        return False

    def get_current_streak(
            self, frequency: str, completions: List[date],
            completion_deletion_date: date = None,
            sample_data: bool = False
    ) -> int | None:
        """
        Calculates the current streak of the selected habit based on habit frequency and completion dates.

        CASE 1. For normal app usage with "Complete for TODAY":
        - duplicate completion check
        - checks is_streak_broken
            - if broken: is_streak_broken method handles streak calculations
            - if not broken: perform streak calculations: - current_streak += 1
                                                          - longest_streak check

        CASE 2. For sample data generation OR "Complete habit PAST" OR "DELETE completion":
        - duplicate completions checks: - sample data has only unique dates
                                        - manager_completions_db.py handles for: - Complete habit PAST
                                                                                 - DELETE completion
        - skips is_streak_broken

            - completion_dates.append(completion_date) performed:
                - for sample data:       -> _generate_completions in sample_data.py <-
                - for past completion:   -> complete_habit_past in Database <-

            - completion_dates.remove(completion_date) performed:
                - for delete completion: -> delete_completion in Database <-

        - processes all completions at once
        - calculates: - current_streak: int
                      - longest_streak: int
                      - broken_streak_lengths: List[]

        Args:
            frequency: The frequency of the habit ("daily" or "weekly").
            completions: List of completion dates.
                         They are passed from the Habits object which owns the Streaks instance.
            completion_deletion_date: CASE 1: Defaults to today if None.
                                      CASE 2: Optional date to mark completion for:
                                            - sample data generation
                                            - complete habit past
                                            - delete a completion
            sample_data: Set to True to activate CASE 2 for sample data generation.
        Returns:
            The current streak count.
        """
        # If no completions, current streak is 0
        if not completions:
            self.current_streak = 0
            return self.current_streak

        # Start with at least 1 since we passed 0 completions check
        self.current_streak = 1

        # CASE 1. Normal app usage behavior
        # => check if streak is broken
        # => calculate streak based on today
        if not completion_deletion_date and sample_data is False:
            if self.is_streak_broken(frequency, completions):
                # If streak is broken:
                #   - current_streak = 1
                #   - the broken streak length was added to it's the list
                return self.current_streak
            else:
                # If streak isn't broken, calculate streaks
                new_streak = self._get_current_streak_case_1(frequency, completions)
                return new_streak

        # Case 2.
        # => no broken streak check
        # => analyze all completions at once

        if sample_data is True or completion_deletion_date:
            new_streak = self._get_current_streak_case_2(frequency, completions)
            return new_streak

    def _get_current_streak_case_1(self, frequency: str, completions: List[date]) -> int:

        # Sort completions to process them chronologically
        sorted_completions = sorted(completions)

        if frequency == "daily":
            # Iterate backwards
            #   starting with last index
            #   stopping before the first index
            #   with a step of -1
            for i in range(len(sorted_completions) - 1, 0, -1):
                # [i-1] will now compare also the first indexed completion
                # If completions are 1 day apart
                days_diff = (sorted_completions[i] - sorted_completions[i-1]).days
                if  days_diff == 1:
                    # Increment count by 1 for each consecutive days
                    self.current_streak += 1
                # If completions aren't 1 day apart
                else:
                    break # Current streak goes back to 1

        elif frequency == "weekly":
            # Iterate backwards through completions to count consecutive weeks
            for i in range(len(sorted_completions) - 1, 0, -1):
                # Get Mondays for current and previous completions
                current_monday = sorted_completions[i] - timedelta(days=sorted_completions[i].weekday())
                previous_monday = sorted_completions[i-1] - timedelta(days=sorted_completions[i-1].weekday())

                weeks_diff = (current_monday - previous_monday).days
                # If completion Mondays are 1 week apart
                if weeks_diff == 7:
                    # Increment count by 1 for each consecutive week
                    self.current_streak += 1
                # If completions aren't 1 week apart
                else:
                    break # Current streak goes back to 1

        # Update the longest streak if current streak is longer
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak

        return self.current_streak

    def _get_current_streak_case_2(self, frequency: str, completions: List[date]) -> int:

        # Sort completions to process them chronologically
        sorted_completions = sorted(completions)

        # Collect all streaks (including broken ones)
        streaks = []
        # Start counting the first completion as a streak of 1
        current_streak = 1

        if frequency == "daily":
            # Iterate through completions and identify streak sequences
            for i in range(1, len(sorted_completions)):
                # Calculate gap between consecutive completions
                days_diff = (sorted_completions[i] - sorted_completions[i - 1]).days

                if days_diff == 1:
                    # If completions are consecutive, extend the streak
                    current_streak += 1
                else:
                    # A gap => a broken streak
                    # Record the length and restart the streak
                    streaks.append(current_streak)
                    current_streak = 1

            # Add the final streak to the list
            streaks.append(current_streak)

        elif frequency == "weekly":
            for i in range(1, len(sorted_completions)):
                # Calculate the Monday of each completion's week
                current_monday = sorted_completions[i] - timedelta(days=sorted_completions[i].weekday())
                previous_monday = sorted_completions[i - 1] - timedelta(days=sorted_completions[i - 1].weekday())

                if (current_monday - previous_monday).days == 7:
                    # If completions are on consecutive weeks, extend the streak
                    current_streak += 1
                else:
                    # A gap => broken streak
                    # Record the length and restart the streak
                    streaks.append(current_streak)
                    current_streak = 1

            # Add the final streak to the list
            streaks.append(current_streak)

        # Process collected streak data
        # - last item is the current active streak
        # - all other items are previously broken streaks
        # - the max value is the longest streak
        self.current_streak = streaks[-1]
        self.broken_streak_lengths = streaks[:-1]  # All except last one
        self.longest_streak = max(streaks)

        return self.current_streak

    def get_longest_streak(self) -> int:
        """
        Gets the longest streak achieved for the selected habit.

        Returns:
            The longest streak count.
        """
        return self.longest_streak