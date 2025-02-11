from datetime import datetime, timedelta
# from habit import Habit
from corpus_meta_lunae.streaks import Streaks

from datetime import datetime, timedelta
from corpus_meta_lunae.streaks import Streaks


def test_broken_streak():
    streaks = Streaks()
    today = datetime.now().date()

    completions = [
        today - timedelta(days=2),
        today - timedelta(days=1),
        today
    ]

    sorted_completions = streaks._sort_completions(completions)

    # Ensure the completions are sorted correctly
    assert sorted_completions == sorted(completions), "Completions are not sorted correctly."

    # Calculate the current streak
    streaks.calculate_current_streak("daily", completions)

    # Check if the current streak is calculated correctly
    assert streaks.current == 3, f"Expected streak of 3, but got {streaks.current}"

    print("Test passed: Current streak is correctly calculated.")

