import unittest
from corpus_meta_lunae.user_database import UserDatabase
from corpus_meta_lunae.user import User
from corpus_meta_lunae.habit import Habit
from corpus_meta_lunae.analytics import Analytics

def test_longest_streak_for_habit():
    # Arrange: Create a mock user with habits
    user = User(username="john_doe")
    habit1 = Habit()
    habit1.name = "Exercise"
    habit1.frequency = "daily"
    habit1.streaks.current_streak = 14  # Assume the current streak is 14
    habit1.streaks.longest_streak = 20  # Assume the longest streak is 20

    habit2 = Habit()
    habit2.name = "Reading"
    habit2.frequency = "weekly"
    habit2.streaks.current_streak = 5
    habit2.streaks.longest_streak = 10

    user.habits = [habit1, habit2]

    # Act: Create Analytics instance and call the method
    analytics = Analytics(user)
    result = analytics.longest_streak_for_habit("Exercise")

    # Assert: Verify that the longest streak for 'Exercise' is returned correctly
    assert result == 20, f"Expected longest streak to be 20, but got {result}"
