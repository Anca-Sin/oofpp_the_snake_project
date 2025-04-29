"""
Unit testing module for the HabitTracker application.

Coverage:
- user and habit functionality: creation, completion, streaks
- analytics functionality: all methods of the analytics module

Note: Some functions (like habit deletion through CLI) require user input
      and have been tested manually due to their interactive nature and db dependencies.
"""

import unittest
from datetime import datetime, timedelta

from core.user import User
from core.habit import Habit
from core.streaks import Streaks
from core.analytics import Analytics

# --------------------------
# User related tests
# --------------------------

class TestUser(unittest.TestCase):
    """Tests the User class functionality."""

    def test_user(self):
        print(f"\n==========================")
        print("Testing User functionality")
        print("--------------------------")

        # Setup
        # -----
        self.user = User()
        self.user.username = "Test User"
        self.user.habits = []

        self.assertEqual(self.user.username, "Test User")
        self.assertEqual(self.user.habits, [])
        print(f"✓ User creation verified!")

# --------------------------
# Habit related tests
# --------------------------

class TestHabitAndCompletions(unittest.TestCase):

    """Tests the Habit class and completions manager functionality."""

    def test_habit(self):
        print(f"\n===========================")
        print("Testing Habit functionality")
        print("---------------------------")

        # Setup
        # -----
        self.habit = Habit()
        self.habit.name = "Test Habit"
        self.habit.frequency = "daily"
        self.habit.creation = datetime.now().date()
        self.habit.completion_dates = []

        # Get current day for testing
        self.today = datetime.now().date()
        self.yesterday = self.today - timedelta(days=1)
        self.two_days_ago = self.today - timedelta(days=2)
        self.last_week = self.today - timedelta(days=7)

        self.assertEqual(self.habit.name, "Test Habit")
        self.assertEqual(self.habit.frequency, "daily")
        self.assertEqual(self.habit.completion_dates, [])
        print(f"✓ Habit creation verified!")

        # Test habit completion for daily habits
        # --------------------------------------
        from db_and_managers.manager_completion_db import _is_habit_completed
        # New Setup
        daily_habit = Habit()
        daily_habit.name = "Daily Test"
        daily_habit.frequency = "daily"
        daily_habit.completion_dates = []

        # Initially not completed
        self.assertFalse(_is_habit_completed(daily_habit))

        # Add today
        daily_habit.completion_dates.append(self.today)

        # Should be completed now
        self.assertTrue(_is_habit_completed(daily_habit))

        # Reset completions and check with yesterday's date only
        daily_habit.completion_dates = [self.yesterday]
        # Shouldn't be completed
        self.assertFalse(_is_habit_completed(daily_habit))
        print(f"✓ Habit daily completion verified!")

        # Tests habit completion for weekly habits
        #-----------------------------------------
        # Avoid circular imports
        from db_and_managers.manager_completion_db import _is_habit_completed
        # New Setup
        weekly_habit = Habit()
        weekly_habit.name = "Weekly Test"
        weekly_habit.frequency = "weekly"
        weekly_habit.completion_dates = []

        # Set the habit as weekly
        weekly_habit.frequency = "weekly"

        # Initially not completed
        self.assertFalse(_is_habit_completed(weekly_habit))

        # Add today
        weekly_habit.completion_dates.append(self.today)

        # Should be completed for this week
        self.assertTrue(_is_habit_completed(weekly_habit))

        # Reset completions and add last week's completion
        weekly_habit.completion_dates = [self.last_week]
        # Shouldn't be completed
        self.assertFalse(_is_habit_completed(weekly_habit))
        print(f"✓ Habit weekly completion verified!")

# --------------------------
# Streaks related tests
# --------------------------

class TestStreaks(unittest.TestCase):
    """Tests the Streaks class functionality."""

    def test_streaks(self):
        print(f"\n=============================")
        print("Testing Streaks functionality")
        print("-----------------------------")

        # Setup
        # -----
        self.streaks = Streaks()
        self.streaks.current_streak = 0
        self.streaks.longest_streak = 0
        self.streaks.broken_streak_length = []

        # Test the is_streak_broken method for daily habits
        # -------------------------------------------------
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        two_days_ago = today - timedelta(days=2)

        # Create a list with yesterday as the last completion
        completions = [two_days_ago, yesterday]

        # Streak should not be broken if last completion was yesterday
        self.assertFalse(self.streaks._is_streak_broken("daily", completions))

        # Create a list with two_days_ago as the last completion
        completions = [two_days_ago]

        # Streak should be broken if last completion was 2 days ago
        self.assertTrue(self.streaks._is_streak_broken("daily", completions))
        print(f"✓ Is daily streak broken verified!")

        # Test the is_streak_broken method for weekly habits
        # --------------------------------------------------
        today = datetime.now().date()
        last_week = today - timedelta(days=7)
        two_weeks_ago = today - timedelta(days=14)

        # Create a list with last_week as the last completion
        completions = [two_weeks_ago, last_week]

        # Streak should not be broken if last completion was 1 week ago
        self.assertFalse(self.streaks._is_streak_broken("weekly", completions))

        # Create a list with two_weeks_ago as the last completion
        completions = [two_weeks_ago]

        # Streak should be broken if last completion was 2 weeks ago
        self.assertTrue(self.streaks._is_streak_broken("weekly", completions))
        print(f"✓ Is weekly streak broken verified!")

        # Test the get_current_streak method for consecutive daily completions
        # --------------------------------------------------------------------
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        two_days_ago = today - timedelta(days=2)

        # Build consecutive completions list
        completions = [two_days_ago, yesterday, today]

        # Test the streak calculations
        result = self.streaks.get_current_streak("daily", completions, sample_data=True)

        # Verify streak calculations
        self.assertEqual(result, 3)
        self.assertEqual(self.streaks.current_streak, 3)
        self.assertEqual(self.streaks.longest_streak, 3)
        self.assertEqual(self.streaks.broken_streak_lengths, [])
        print(f"✓ Current streak consecutive daily completions verified!")

        # Test the get_current_streak method for non-consecutive daily completions
        # ------------------------------------------------------------------------
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        three_days_ago = today - timedelta(days=3)

        # Test with a gap in completions
        completions = [three_days_ago, yesterday, today]

        # Calculate streaks using sample_data mode
        result = self.streaks.get_current_streak("daily", completions, sample_data=True)

        # The current streak should be 2 (yesterday and today)
        self.assertEqual(result, 2)
        self.assertEqual(self.streaks.current_streak, 2)
        self.assertEqual(self.streaks.longest_streak, 2)
        self.assertEqual(self.streaks.broken_streak_lengths, [1])
        print(f"✓ Current streak non-consecutive daily completions verified!")

        # Test the get_current_streak method for consecutive weekly completions
        # ---------------------------------------------------------------------
        today = datetime.now().date()
        last_week = today - timedelta(days=7)
        two_weeks_ago = today - timedelta(days=14)

        # Build consecutive weekly completions
        completions = [two_weeks_ago, last_week, today]

        # Calculate streaks
        result = self.streaks.get_current_streak("weekly", completions, sample_data=True)

        # Verify streak calculations
        self.assertEqual(result, 3)
        self.assertEqual(self.streaks.current_streak, 3)
        self.assertEqual(self.streaks.longest_streak, 3)
        self.assertEqual(self.streaks.broken_streak_lengths, [])
        print(f"✓ Current streak consecutive weekly completions verified!")

        # Test the get_current_streak method for non-consecutive weekly completions
        # -------------------------------------------------------------------------
        today = datetime.now().date()
        last_week = today - timedelta(days=7)
        three_weeks_ago = today - timedelta(days=21)

        # Test with a gap in weekly completions
        completions = [three_weeks_ago, last_week, today]

        # Calculate streaks
        result = self.streaks.get_current_streak("weekly", completions, sample_data=True)

        # The current streak should be 2 (last week and today)
        self.assertEqual(result, 2)
        self.assertEqual(self.streaks.current_streak, 2)
        self.assertEqual(self.streaks.longest_streak, 2)
        self.assertEqual(self.streaks.broken_streak_lengths, [1])
        print(f"✓ Current streak non-consecutive weekly completions verified!")

# --------------------------
# Analytics related tests
# --------------------------

class TestAnalytics(unittest.TestCase):
    """Tests the Analytics class functionality."""

    def test_analytics(self):
        print(f"\n===============================")
        print("Testing Analytics functionality")
        print("-------------------------------")

        # Setup
        # -----
        # Create test user
        self.user = User(username="Test User")

        # Create test habits
        habit1 = Habit()
        habit1.name = "Daily Exercise"
        habit1.frequency = "daily"

        habit2 = Habit()
        habit2.name = "Weekly Review"
        habit2.frequency = "weekly"

        # Add completions
        today = datetime.now().date()

        habit1.completion_dates = [
            today,
            today - timedelta(days=1),     # Yesterday
            today - timedelta(days=2),     # Two days ago
            today - timedelta(days=3)      # Three days ago
        ]
        habit1.streaks.current_streak = 4
        habit1.streaks.longest_streak = 4

        habit2.completion_dates = [
            today - timedelta(days=2),     # This week
            today - timedelta(days=9),     # Last week
            today - timedelta(days=16)     # Two weeks ago
        ]
        habit2.streaks.current_streak = 3
        habit2.streaks.longest_streak = 3

        # Add habits to user
        self.user.habits = [habit1, habit2]

        # Create analytics
        self.analytics = Analytics(self.user)

        # Test retrieving all habits for a user
        # -------------------------------------
        habits = self.analytics.list_all_habits()

        self.assertEqual(len(habits), 2)
        self.assertEqual(habits[0].name, "Daily Exercise")
        self.assertEqual(habits[1].name, "Weekly Review")
        print(f"✓ List all habits verified!")

        # Tests retrieving habits by periodicity
        # --------------------------------------
        daily_habits = self.analytics.list_habits_by_periodicity("daily")
        weekly_habits = self.analytics.list_habits_by_periodicity("weekly")

        self.assertEqual(len(daily_habits), 1)
        self.assertEqual(daily_habits[0].name, "Daily Exercise")

        self.assertEqual(len(weekly_habits), 1)
        self.assertEqual(weekly_habits[0].name, "Weekly Review")
        print(f"✓ List all habits by periodicity verified!")

        # Test retrieving the longest streak across all habits
        # ----------------------------------------------------
        habit_name, streak = self.analytics.longest_streak_all_habits()

        self.assertEqual(streak, 4)
        self.assertEqual(habit_name, "Daily Exercise")
        print(f"✓ Longest streak across all habit verified!")

        # Test retrieving the longest streak for one habit
        # ------------------------------------------------
        # Test for habit 1
        longest_streak_habit_1 = self.analytics.longest_streak_for_habit("Daily Exercise")
        self.assertEqual(longest_streak_habit_1, 4)

        # Test for habit 2
        longest_streak_habit_2 = self.analytics.longest_streak_for_habit("Weekly Review")
        self.assertEqual(longest_streak_habit_2, 3)
        print(f"✓ Longest streak for a selected habit verified!")

        # Tests retrieving the longest streak as a tuple of (name, streak)
        # ----------------------------------------------------------------
        # Test daily habits
        daily_name, daily_streak = self.analytics.longest_streak_by_periodicity("daily")
        self.assertEqual(daily_name, "Daily Exercise")
        self.assertEqual(daily_streak, 4)

        # Test weekly habits
        weekly_name, weekly_streak = self.analytics.longest_streak_by_periodicity("weekly")
        self.assertEqual(weekly_name, "Weekly Review")
        self.assertEqual(weekly_streak, 3)
        print(f"✓ Longest streak by periodicity verified!")

        # Test retrieving the most and least completed habits as a tuple of (name, completions count)
        # -------------------------------------------------------------------------------------------
        # Test most completed habit
        most_name, most_count = self.analytics.most_completed_habit()
        self.assertEqual(most_name, "Daily Exercise")
        self.assertEqual(most_count, 4)
        print(f"✓ Most completed habit across all habits verified!")

        # Test least completed habit
        least_name, least_count = self.analytics.least_completed_habit()
        self.assertEqual(least_name, "Weekly Review")
        self.assertEqual(least_count, 3)
        print(f"✓ Least completed habit across all habits verified!")

        # Test retrieving the most completed habit by periodicity as a tuple of (name, completions count)
        # -----------------------------------------------------------------------------------------------
        # Test daily habits
        daily_name, daily_count = self.analytics.most_completed_by_periodicity("daily")
        self.assertEqual(daily_name, "Daily Exercise")
        self.assertEqual(daily_count, 4)

        # Test weekly habits
        weekly_name, weekly_count = self.analytics.most_completed_by_periodicity("weekly")
        self.assertEqual(weekly_name, "Weekly Review")
        self.assertEqual(weekly_count, 3)
        print(f"✓ Most completed habit by periodicity verified!")

        # Test retrieving the least completed habit by periodicity as a tuple of (name, completions count)
        # ------------------------------------------------------------------------------------------------
        # Test daily habits
        daily_name, daily_count = self.analytics.least_completed_by_periodicity("daily")
        self.assertEqual(daily_name, "Daily Exercise")
        self.assertEqual(daily_count, 4)

        # Test weekly habits
        weekly_name, weekly_count = self.analytics.least_completed_by_periodicity("weekly")
        self.assertEqual(weekly_name, "Weekly Review")
        self.assertEqual(weekly_count, 3)
        print(f"✓ Least completed habit by periodicity verified!")

        # Test calculating the average streak length for a habit
        # ------------------------------------------------------
        # Test for habit 1
        avg_habit_1 = self.analytics.average_streak_length_habit("Daily Exercise")
        self.assertEqual(avg_habit_1, 4)

        # Test for habit 2
        avg_habit_2 = self.analytics.average_streak_length_habit("Weekly Review")
        self.assertEqual(avg_habit_2, 3)
        print(f"✓ Average streak length for a selected habit verified!")

        # Test calculating the average streak length across all habits
        # ------------------------------------------------------------
        avg = self.analytics.average_streak_all_habits()
        self.assertEqual(avg, 3.5)
        print(f"✓ Average streak length across all habits verified!")

        # Test calculating the average streak length for habits by periodicity
        # --------------------------------------------------------------------
        daily_avg = self.analytics.average_streak_by_periodicity("daily")
        self.assertEqual(daily_avg, 4)

        weekly_avg = self.analytics.average_streak_by_periodicity("weekly")
        self.assertEqual(weekly_avg, 3)
        print(f"✓ Average streak length by periodicity verified!")

if __name__ == "__main__":
    unittest.main()