"""
Unit testing module for Streaks and Analytics on submission data.
"""

import unittest

from core.analytics import Analytics
from db_and_managers.database import Database

class TestStreaksSampleData(unittest.TestCase):
    """Tests streaks functions with submission sample data."""
    def test_streaks_with_sample_data(self):
        print(f"\n==========================================")
        print("Testing Streaks for Submission Sample Data")
        print("------------------------------------------")
        db = Database()
        users = db.load_users()

        # Find SampleUser in the list -> it exists as per task requirement
        sample_user = next(user for user in users if user.username == "SampleUser")

        # Load habits for SampleUser
        db.load_habits(sample_user)

        # Defining expected values based on the sample data used for submission
        expected_data = {
            "Morning Meditation": {
                "current_streak": 3,
                "longest_streak": 6,
                "broken_streak_lengths": [2, 2, 6, 1, 6]
            },
            "Read 30 Minutes": {
                "current_streak": 7,
                "longest_streak": 12,
                "broken_streak_lengths": [12, 1, 1, 2]
            },
            "Drink 2L Water": {
                "current_streak": 4,
                "longest_streak": 5,
                "broken_streak_lengths": [4, 1, 5, 5, 5]
            },
            "Weekly Planning": {
                "current_streak": 5,
                "longest_streak": 5,
                "broken_streak_lengths": []
            },
            "Deep House Cleaning": {
                "current_streak": 5,
                "longest_streak": 5,
                "broken_streak_lengths": []
            }
        }

        # Check each habit against expected data
        for habit in sample_user.habits:
            if habit.name in expected_data:
                expected = expected_data[habit.name]

                # Assert that values match expected data
                self.assertEqual(habit.streaks.current_streak, expected["current_streak"])
                print(f"✓ Current streak for sample habit {habit.name} verified!")
                self.assertEqual(habit.streaks.longest_streak, expected["longest_streak"])
                print(f"✓ Longest streak for sample habit {habit.name} verified!")
                self.assertEqual(habit.streaks.broken_streak_lengths, expected["broken_streak_lengths"])
                print(f"✓ Broken streak lengths for sample habit {habit.name} verified!")

class TestAnalyticsSampleData(unittest.TestCase):
    """Tests analytics functions with submission sample data."""

    def test_analytics_with_sample_data(self):
        print(f"\n============================================")
        print("Testing Analytics for Submission Sample Data")
        print("--------------------------------------------")
        db = Database()
        users = db.load_users()

        # Find SampleUser in the list -> it exists as per task requirement
        sample_user = next(user for user in users if user.username == "SampleUser")

        # Load habits for SampleUser
        db.load_habits(sample_user)

        # Create a new Analytics instance with sample_user
        sample_analytics = Analytics(sample_user)

        # List all habits
        all_habits = sample_analytics.list_all_habits()
        self.assertEqual(len(all_habits), 5)
        print(f"✓ List all habits for {sample_user.username} verified!")

        # List by periodicity
        daily_habits = sample_analytics.list_habits_by_periodicity("daily")
        self.assertEqual(len(daily_habits), 3)

        weekly_habits = sample_analytics.list_habits_by_periodicity("weekly")
        self.assertEqual(len(weekly_habits), 2)
        print(f"✓ List habits by periodicity {sample_user.username} verified!")

        # Longest streak across all habits
        habit_name, longest_streak = sample_analytics.longest_streak_all_habits()
        self.assertEqual(habit_name, "Read 30 Minutes")
        self.assertEqual(longest_streak, 12)
        print(f"✓ Longest streak across all habits for {sample_user.username} verified!")

        # Longest streak for a selected habit
        longest_streak_selected = sample_analytics.longest_streak_for_habit("Read 30 Minutes")
        self.assertEqual(longest_streak_selected, 12)
        print(f"✓ Longest streak for a selected habit for {sample_user.username} verified!")

        # Longest streak by periodicity
        daily_longest_name, daily_longest_count = sample_analytics.longest_streak_by_periodicity("daily")
        self.assertEqual(daily_longest_name, "Read 30 Minutes")
        self.assertEqual(daily_longest_count, 12)

        weekly_longest_name, weekly_longest_count = sample_analytics.longest_streak_by_periodicity("weekly")
        self.assertEqual(weekly_longest_name, "Deep House Cleaning")
        self.assertEqual(weekly_longest_count, 5)
        print(f"✓ List by periodicity for {sample_user.username} verified!")

        # Most & least completed across all habits
        most_name, most_count = sample_analytics.most_completed_habit()
        self.assertEqual(most_name, "Drink 2L Water")
        self.assertEqual(most_count, 24)
        print(f"✓ Most completed habit across all habits for {sample_user.username} verified!")

        least_name, least_count = sample_analytics.least_completed_habit()
        self.assertEqual(least_name, "Weekly Planning")  # or Deep House Cleaning, both have 5 completions
        self.assertEqual(least_count, 5)
        print(f"✓ Least completed habit across all habits for {sample_user.username} verified!")

        # Most & least completed by periodicity
        daily_most_name, daily_most_count = sample_analytics.most_completed_by_periodicity("daily")
        self.assertEqual(daily_most_name, "Drink 2L Water")
        self.assertEqual(daily_most_count, 24)

        weekly_most_name, weekly_most_count = sample_analytics.most_completed_by_periodicity("weekly")
        self.assertEqual(weekly_most_name, "Deep House Cleaning")
        self.assertEqual(weekly_most_count, 5)

        daily_least_name, daily_least_count = sample_analytics.least_completed_by_periodicity("daily")
        self.assertEqual(daily_least_name, "Morning Meditation")
        self.assertEqual(daily_least_count, 20)

        weekly_least_name, weekly_least_count = sample_analytics.least_completed_by_periodicity("weekly")
        self.assertEqual(weekly_least_name, "Deep House Cleaning")
        self.assertEqual(weekly_least_count, 5)
        print(f"✓ Most & least completed habits by periodicity for {sample_user.username} verified!")

        # Average streak length for a selected habit
        average_selected_habit = round(sample_analytics.average_streak_length_habit("Morning Meditation"), 2)
        self.assertEqual(average_selected_habit, 3.33)
        print(f"✓ Average streak length for a selected habit for {sample_user.username} verified!")

        # Average streak length across all habits
        average_all = round(sample_analytics.average_streak_all_habits(), 2)
        self.assertEqual(average_all, 4.05)
        print(f"✓ Average streak length across all habits for {sample_user.username} verified!")

        # Average streak length by periodicity
        daily_average = round(sample_analytics.average_streak_by_periodicity("daily"), 2)
        self.assertEqual(daily_average, 3.94)

        weekly_average = round(sample_analytics.average_streak_by_periodicity("weekly"), 2)
        self.assertEqual(weekly_average, 5)
        print(f"✓ Average streak length by periodicity for {sample_user.username} verified!")

if __name__ == "__main__":
    unittest.main()