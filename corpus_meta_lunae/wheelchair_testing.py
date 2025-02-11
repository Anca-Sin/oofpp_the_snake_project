from datetime import datetime, timedelta
# from habit import Habit
from corpus_meta_lunae.streaks import Streaks


def test_daily_streak():
    streaks = Streaks()
    today = datetime.now().date()

    # Test consecutive days
    completions = [
        today - timedelta(days=2),
        today - timedelta(days=1),
        today
    ]
    assert streaks.calculate_current_streak("daily", completions) == 3

    # Test broken streak
    broken_completions = [
        today - timedelta(days=3),
        today - timedelta(days=1),
        today
    ]
    assert streaks.calculate_current_streak("daily", broken_completions) == 2