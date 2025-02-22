import unittest
from corpus_meta_lunae.user_database import UserDatabase
from corpus_meta_lunae.user import User
from corpus_meta_lunae.habit import Habit
from corpus_meta_lunae.analytics import Analytics

def test_list_all_habits():
    # Arrange: Create a mock user with habits
    user = User(username="john_doe")
    habit1 = Habit()
    habit1.name = "Exercise"
    habit1.frequency = "daily"

    habit2 = Habit()
    habit2.name = "Reading"
    habit2.frequency = "weekly"

    user.habits = [habit1, habit2]

    # Act: Create Analytics instance and call the method
    analytics = Analytics(user)
    result = analytics.list_all_habits()

    # Assert: Verify that the habit names are returned correctly
    assert result == ["Exercise", "Reading"], f"Expected ['Exercise', 'Reading'], but got {result}"


def test_list_habits_by_periodicity():
    # Arrange: Create a mock user with habits
    user = User(username="john_doe")
    habit1 = Habit()
    habit1.name = "Exercise"
    habit1.frequency = "daily"

    habit2 = Habit()
    habit2.name = "Reading"
    habit2.frequency = "weekly"

    habit3 = Habit()
    habit3.name = "Jogging"
    habit3.frequency = "daily"

    user.habits = [habit1, habit2, habit3]

    # Act: Create Analytics instance and call the method
    analytics = Analytics(user)
    result = analytics.list_habits_by_periodicity("daily")

    # Assert: Verify that the daily habits are returned correctly
    assert result == ["Exercise", "Jogging"], f"Expected ['Exercise', 'Jogging'], but got {result}"