from datetime import datetime, timedelta
# from habit import Habit
from corpus_meta_lunae.streaks import Streaks


def test_longest_streak():
    streaks = Streaks()
    today = datetime.now().date()

    # Create a 2-day longest streak
    completions = [today - timedelta(days=1), today]
    streaks.calculate_current_streak("daily", completions)
    assert streaks.get_longest_streak() == 2

    # Create a 3-day streak
    completions = [
        today - timedelta(days=2),
        today - timedelta(days=1),
        today
    ]
    streaks.calculate_current_streak("daily", completions)
    assert streaks.get_longest_streak() == 3