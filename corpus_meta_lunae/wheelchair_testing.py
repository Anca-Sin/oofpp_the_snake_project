from datetime import datetime, timedelta
# from habit import Habit
from corpus_meta_lunae.streaks import Streaks

def test_weekly_streak():
    streaks = Streaks()
    today = datetime.now().date()

    # Test consecutive weeks (completed on different days within weeks)
    completions = [
        today - timedelta(days=14),  # 2 weeks ago
        today - timedelta(days=7),   # last week
        today                        # this week
    ]
    assert streaks.calculate_current_streak("weekly", completions) == 3

    # Test broken weekly streak
    broken_completions = [
        today - timedelta(days=21),  # 3 weeks ago
        today - timedelta(days=7),   # last week
        today                        # this week
    ]
    assert streaks.calculate_current_streak("weekly", broken_completions) == 2