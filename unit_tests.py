"""
Unit Tests for the HabitTracker application

These tests cover the core functionality of the app:
- User
- Habit
- Streaks
- Analytics
"""

import unittest
from datetime import datetime, timedelta

from core.user import User
from core.habit import Habit
from core.streaks import Streaks
from core.analytics import Analytics

class TestUser(unittest.TestCase):
    """Tests the User class functionality."""

    def setUp(self):
        self.user = User()
        self.user.username = "Test User"
        self.user.habits = []

    def test_user(self):
        """Tests that a user can be created with correct attributes."""
        self.assertEqual(self.user.username, "Test User")
        self.assertEqual(self.user.habits, [])

class TestHabit(unittest.TestCase):
    """Tests the Habit class functionality."""

    def setUp(self):
        self.habit = Habit()
        self.habit.name = "Test Habit"
        self.habit.frequency = "daily"
        self.habit.creation = datetime.now().date()

    def test_habit_creation(self):
        """Tests that a habit can be created with correct attributes."""
        self.assertEqual(self.habit.name, "Test Habit")
        self.assertEqual(self.habit.frequency, "daily")
        self.assertEqual(self.habit.completion_dates, [])

    def test_is_habit_completed_daily(self):
        """Tests the _is_habit_completed method for daily habits."""
        # Initially not completed
        self.assertFalse(self.habit._is_habit_completed())

        # Add today's date to completion_dates
        today = datetime.now().date()
        self.habit.completion_dates.append(today)

        # Now it should be completed
        self.assertTrue(self.habit._is_habit_completed())

    def test_is_habit_completed_weekly(self):
        """Tests the _is_habit_completed method for weekly habits."""
        # Set up habit as weekly
        self.habit.frequency = "weekly"

        # Initially not completed
        self.assertFalse(self.habit._is_habit_completed())

        # Add today's date to completion_dates
        today = datetime.now().date()
        self.habit.completion_dates.append(today)

        # Now it should be completed
        self.assertTrue(self.habit._is_habit_completed())

    def test_check_off_habit(self):
        """Tests the check_off_habit method."""
        # Should succeed first time
        self.assertTrue(self.habit.check_off_habit())

        # Should fail second time (already completed today)
        self.assertFalse(self.habit.check_off_habit())

        # Verify completion was added
        self.assertEqual(len(self.habit.completion_dates), 1)

class TestStreaks(unittest.TestCase):
    """Tests the Streaks class functionality."""

    def setUp(self):
        self.streaks = Streaks()

    def test_is_streak_broken_daily(self):
        """Tests the is_streak_broken method for daily habits."""
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        two_days_ago = today - timedelta(days=2)

        # Streak should not be broken if last completion was yesterday
        self.assertFalse(self.streaks.is_streak_broken("daily", yesterday))

        # Streak should be broken if last completion was 2 days ago
        self.assertTrue(self.streaks.is_streak_broken("daily", two_days_ago))

    def test_is_streak_broken_weekly(self):
        """Tests the is_streak_broken method for weekly habits."""
        today = datetime.now().date()
        last_week = today - timedelta(days=7)
        two_weeks_ago = today - timedelta(days=14)

        # Streak should not be broken if last completion was 1 week ago
        self.assertFalse(self.streaks.is_streak_broken("weekly", last_week))

        # Streak should be broken if last completion was 2 weeks ago
        self.assertTrue(self.streaks.is_streak_broken("weekly", two_weeks_ago))

    def test_current_streak_daily_consecutive(self):
        """Tests the get_current_streak method for consecutive daily completions."""
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        two_days_ago = today - timedelta(days=2)

        # No completion
        self.assertEqual(self.streaks.get_current_streak("daily", []), 0)

        # One completion
        self.assertEqual(self.streaks.get_current_streak("daily", [today]), 1)

        # Consecutive completions
        completions = [two_days_ago, yesterday, today]
        self.assertEqual(self.streaks.get_current_streak("daily", completions), 3)
        self.assertEqual(self.streaks.longest_streak, 3)

    def test_get_current_streak_daily_non_consecutive(self):
        """Tests the get_current_streak method for non-consecutive daily completions."""
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        three_days_ago = today - timedelta(days=3)

        # Streak should be reset after the gap

        completions = [three_days_ago, yesterday, today]

        # First call should add broken_streak_length=1 and reset current_streak=0
        broken = self.streaks.get_current_streak("daily", [three_days_ago])
        self.assertEqual(broken, 0)

        # Second call should start a new streak with yesterday and today
        self.assertEqual(self.streaks.get_current_streak("daily", completions), 2)
        self.assertEqual(self.streaks.longest_streak, 2)
        self.assertEqual(self.streaks.broken_streak_length, [1])

    def test_get_current_streak_weekly(self):
        """Tests the get_current_streak method for weekly completions."""
        today = datetime.now().date()
        last_week = today - timedelta(days=7)
        two_weeks_ago = today - timedelta(days=14)

        # Consecutive weekly completions
        completions = [two_weeks_ago, last_week, today]
        self.assertEqual(self.streaks.get_current_streak("weekly", completions), 3)
        self.assertEqual(self.streaks.longest_streak, 3)

class TestAnalytics(unittest.TestCase):
    """Tests the Analytics class functionality."""

    def setUp(self):
        # Create test user
        self.user = User(username="Test User")

        # Create test habits
        habit1 = Habit()
        habit1.name = "Daily Exercise"
        habit1.frequency = "daily"
        habit1.creation = datetime.now().date() - timedelta(days=10)

        habit2 = Habit()
        habit2.name = "Weekly Review"
        habit2.frequency = "weekly"
        habit2.creation = datetime.now().date() - timedelta(days=21)

        # Add completions
        today = datetime.now().date()

        habit1.completion_dates = [
            today,
            today - timedelta(days=1),
            today - timedelta(days=2)
        ]
        habit1.streaks.current_streak = 3
        habit1.streaks.longest_streak = 3

        habit2.completion_dates = [
            today - timedelta(days=2),
            today - timedelta(days=9),
            today - timedelta(days=16)
        ]
        habit2.streaks.current_streak = 3
        habit2.streaks.longest_streak = 3

        # Add habits to user
        self.user.habits = [habit1, habit2]

        # Create analytics
        self.analytics = Analytics(self.user)

    def test_list_all_habits(self):
        """Tests the list_all_habits method."""
        habits = self.analytics.list_all_habits()

        # Should return all habits
        self.assertEqual(len(habits), 2)
        self.assertEqual(habits[0].name, "Daily Exercise")
        self.assertEqual(habits[1].name, "Weekly Review")

    def test_list_habits_by_periodicity(self):
        """Tests the list_habits_by_periodicity method."""
        daily_habits = self.analytics.list_habits_by_periodicity("daily")
        weekly_habits = self.analytics.list_habits_by_periodicity("weekly")

        # Should filter correctly
        self.assertEqual(len(daily_habits), 1)
        self.assertEqual(daily_habits[0].name, "Daily Exercise")

        self.assertEqual(len(weekly_habits), 1)
        self.assertEqual(weekly_habits[0].name, "Weekly Review")

    def test_longest_streak_all_habits(self):
        """Tests the longest_streak_all_habits method."""
        habit_name, streak = self.analytics.longest_streak_all_habits()

        # Both habits have a streak of 3, so could be either one
        self.assertEqual(streak, 3)
        self.assertIn(habit_name, ["Daily Exercise", "Weekly Review"])

    def test_longest_streak_for_habit(self):
        """Tests the longest_streak_for_habit method."""
        habit_name, streak = self.analytics.longest_streak_for_habit("Daily Exercise")

        self.assertEqual(habit_name, "Daily Exercise")
        self.assertEqual(streak, 3)

    def test_most_least_completed_habit(self):
        """Tests both most and least completed habit analytics."""
        # Add more completions for the daily habit
        today = datetime.now().date()
        self.user.habits[0].completion_dates.append(today - timedelta(days=3))

        # Test most completed habit
        most_name, most_count = self.analytics.most_completed_habit()
        self.assertEqual(most_name, "Daily Exercise")
        self.assertEqual(most_count, 4)

        # Test least completed habit
        least_name, least_count = self.analytics.least_completed_habit()
        self.assertEqual(least_name, "Weekly Review")
        self.assertEqual(least_count, 3)

if __name__ == "__main__":
    unittest.main()