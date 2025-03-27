from datetime import datetime, timedelta, date
from typing import List

class Streaks:
    """
    Tracks streak information for each habit.

    - handles the logic for determining and storing:
            - current streak, by refactoring into two helper methods:
                    - CASE 1. For incremental calculations with today's date
                    - CASE 2. For batch calculations across all completion dates
            - longest streak
    - keeps a history of broken streaks
    - uses helper method to check if a streak is broken for CASE 1
    - has no direct db dependency:
            streaks are directly linked to their habit through foreign keys relationships in the db

    Attributes:
        current_streak:        An integer as the count of consecutive completions for a habit.
        longest_streak:        An integer as the longest streak achieved for a habit.
        broken_streak_lengths: A list of integers as the history of streak lengths when they were broken.
    """

    def __init__(self):
        """Initializes the Streaks instance."""
        self.current_streak: int = 0
        self.longest_streak: int = 0
        self.broken_streak_lengths: List[int] = []

    def _is_streak_broken(self, frequency: str, completion_dates: List[date]) -> bool:
        """
        Determines if a streak is broken based on the frequency and latest completion date.

        See get_current_streak() for full arguments' documentation.

        - checks if the streak is broken
        - if yes, it adds the current streak length to the broken_streak_lengths history
        - then resets the current_streak to 1

        Args:
            frequency:        The habit frequency.
            completion_dates: List of completion dates.
                              They are passed from the Habits object which owns the Streaks instance.
        Returns:
            True if streak is broken, False if still active streak.
        """
        today = datetime.now().date()

        sorted_completion_dates = sorted(completion_dates)
        last_completion = sorted_completion_dates[-1]

        if frequency == "daily":
            # Streak is broken if more than 1 day has passed since last completion
            if (today - last_completion).days > 1:
                # Save broken streak length to the list
                self.broken_streak_lengths.append(self.current_streak)
                # Reset current streak to today's completion
                self.current_streak = 1
                return True # Streak is broken

        elif frequency == "weekly":
            # Calculate the Monday of the current week
            current_week_monday = today - timedelta(days=today.weekday()) # weekday() -> 0 for Monday

            # Calculate the Monday of the week of the last completion
            last_completion_week_monday = last_completion - timedelta(days=last_completion.weekday())

            # Streak is broken if current week's Monday is more than 7 days apart from the latest completion's Monday
            if current_week_monday > last_completion_week_monday + timedelta(days=7):
                # Save broken streak length to the list
                self.broken_streak_lengths.append(self.current_streak)
                # Reset current streak to today's completion
                self.current_streak = 1
                return True # Streak is broken

        return False # Streak isn't broken

    def _get_current_streak_case_1(self) -> int:
        """
        Increments current streak by 1 and updates longest streak if needed.

        Handles CASE 1 in get_current_streak().

        - duplicate completion dates checks: manager_completions_db.py handles it through complete_habit_today()
        - relies on _is_streak_broken() logic: called in main method only when _is_streak_broken() -> False
                                               = meaning streak is still active

        Returns:
            An integer representing the current streak length in days.
        """
        self.current_streak += 1

        # Update the longest streak if needed
        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak

        return self.current_streak

    def _get_current_streak_case_2(self, frequency: str, completion_dates: List[date]) -> int:
        """
        Processes all completion dates entirely.

        Handles CASE 2 in get_current_streak().
        See get_current_streak() for full arguments' documentation.

        - duplicate completion dates checks:
                              - sample data generates only unique dates
                              - manager_completions_db.py handles through: - complete_habit_past()
                                                                           - delete_completion()
        - doesn't rely on _is_streak_broken() logic
        - iterates through all completion dates and:
                              - recalculates all streaks
                              - stores the broken streak lengths
                              - recalculates the longest streak
        Args:
            frequency:        The habit frequency.
            completion_dates: List of completion dates.

        Returns:
            An integer representing the current streak length in days.
        """
        # Sort completion dates to process them chronologically
        sorted_completion_dates = sorted(completion_dates)

        # Collect all streaks (including broken ones)
        streaks = []
        # Start counting the first completion as a streak of 1
        current_streak = 1

        if frequency == "daily":
            # Iterate through completion dates to identify streak sequences
            for i in range(1, len(sorted_completion_dates)):

                # Calculate gap between consecutive completion dates
                days_diff = (sorted_completion_dates[i] - sorted_completion_dates[i - 1]).days

                # If completion dates are on consecutive days
                if days_diff == 1:
                    current_streak += 1 # Extend the streak

                # A gap => a broken streak
                else:
                    streaks.append(current_streak) # Record the length
                    current_streak = 1 # Restart the streak

            # Add the final streak to the list
            streaks.append(current_streak)

        elif frequency == "weekly":
            # Iterate through completion dates to identify streak sequences
            for i in range(1, len(sorted_completion_dates)):

                # Calculate the Monday of each completion's week
                current_monday = sorted_completion_dates[i] - timedelta(days=sorted_completion_dates[i].weekday())
                previous_monday = sorted_completion_dates[i - 1] - timedelta(days=sorted_completion_dates[i - 1].weekday())

                # If completion dates are on consecutive weeks
                if (current_monday - previous_monday).days == 7:
                    current_streak += 1 # Extend the streak

                # A gap => broken streak
                else:
                    streaks.append(current_streak) # Record the length
                    current_streak = 1 # Restart the streak

            # Add the final streak to the list
            streaks.append(current_streak)

        # Process the collected streak data:
        # - last item is the current active streak
        self.current_streak = streaks[-1]
        # - all other items are previously broken streaks
        self.broken_streak_lengths = streaks[:-1]  # All except last one
        # - the max value is the longest streak
        self.longest_streak = max(streaks)

        return self.current_streak

    def get_current_streak(
            self,
            frequency: str,
            completion_dates: List[date],
            completion_deletion_date: date = None,
            sample_data: bool = False
    ) -> int | None:
        """
        Deploys main streak calculations logic.

        - analyzes completion dates according to the habit's frequency
        - refactored into 2 helper methods:

                - CASE 1: - light logic used for - "Complete habit TODAY"
                          - simply increments current_streak by 1 if the streak isn't broken

                - CASE 2: - heavy logic used for -  Sample Data
                                                 - "Complete habit PAST"
                                                 - "DELETE Completion"
                          - recalculates streaks entirely

        - takes parameters "completion_deletion_date" and "sample_data", which allow enabling CASE 2 accordingly

        Args:
            frequency:
                How often the habit should be completed ("daily" or "weekly").
                (passed from the Habit object which owns the Streaks instance)
            completion_dates:
                List of completion dates.
                (passed from the Habits object which owns the Streaks instance)
            completion_deletion_date:
                CASE 1: Disabled  - Set to None
                CASE 2: Activated - Date to mark past completion or to remove a completion.
            sample_data:
                CASE 1: Disabled  - Set to False.
                CASE 2: Activated - Set to True.
        Returns:
            An integer representing the current streak length in days.
        """
        # If no completion dates, current streak is 0
        if not completion_dates:
            self.current_streak = 0
            return self.current_streak

        # Start record at 0
        self.current_streak = 0

        # CASE 1: complete today
        if sample_data is False and not completion_deletion_date: # disable CASE 2 parameters
            if self._is_streak_broken(frequency, completion_dates):
                # If streak is broken, calculations are handled internally in _is_streak_broken()
                return self.current_streak
            else:
                # If streak isn't broken
                # Call case_1 helper
                new_streak = self._get_current_streak_case_1()
                return new_streak

        # CASE 2: sample data, complete past, delete completion
        if sample_data is True or completion_deletion_date: # enable CASE 2 parameters
            # Call case_2 helper
            new_streak = self._get_current_streak_case_2(frequency, completion_dates)
            return new_streak


    def get_longest_streak(self) -> int:
        """
        The longest streak of a habit.

        Returns:
            An integer representing the longest streak count in days.
        """
        return self.longest_streak