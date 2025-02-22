import unittest
from corpus_meta_lunae.user_database import UserDatabase
from corpus_meta_lunae.user import User
from corpus_meta_lunae.habit import Habit
from corpus_meta_lunae.analytics import Analytics


def test_longest_streak_all_habits():
    # Arrange: Create a mock user with habits
    user = User(username="john_doe")

    habit1 = Habit()
    habit1.name = "Exercise"
    habit1.frequency = "daily"
    habit1.streaks.longest_streak = 20  # Set the longest streak to 20

    habit2 = Habit()
    habit2.name = "Reading"
    habit2.frequency = "weekly"
    habit2.streaks.longest_streak = 15  # Set the longest streak to 15

    user.habits = [habit1, habit2]

    # Act: Create Analytics instance and call the method
    analytics = Analytics(user)
    result = analytics.longest_streak_all_habits()

    # Assert: Verify that the habit with the longest streak ('Exercise') is returned with the correct streak (20)
    assert result == ('Exercise', 20), f"Expected ('Exercise', 20), but got {result}"


