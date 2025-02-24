from ssl import CHANNEL_BINDING_TYPES

from .analytics import Analytics
from .user_database import UserDatabase


class HabitTracker:
    """
    Main class to manage users, habit creation and tracking, streaks, and analytics.
    """

    def __init__(self):
        """
        Initializes the habit tracker.
        - Connects to the UserDatabase (handles storage and retrieval)
        - Optionally handles multiple users, but no login required (just for my exercise)
        """
        self.db = UserDatabase()   # Interacts with the local SQLite DB
        self.logged_in_user = None # Hypothetical "logged_in"

    def start(self):

    def select_user(self):

    def load_user_data(self):

    def main_menu(self):
        # I. My habits
        # II. My Analytics
        #
        # I. My habits
        #     1. Register New Habit  *
        #     2. List All My Habits  *
        #     3. My Daily Habits     *
        #     4. My Weekly Habits    *
        #
        #         * when selecting a Habit:
        #             - {habit} Completions: - Mark as complete: - today
        #                                                        - a previous date
        #                                    - Remove a completion
        #             - {habit} Analytics: - creation date
        #                                  - current streak
        #                                  - longest streak
        #                                  - average streak length
        #                                  - all-time completions count
        #
        # II. My Analytics
        #     1. Longest streak all habits
        #     2. Most completed habit
        #     3. Least completed habit
