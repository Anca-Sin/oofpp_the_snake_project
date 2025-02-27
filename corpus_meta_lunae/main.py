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

    def start(self) -> None:
        """
        Starts the Habit Tracker app.
        - Greets the user and allows username selection, or allows creating a new user
        - After the selection, the main menu is displayed
        """
        print("-- 'Corpus Meta Lunae' -- Habit Tracker --")

        # Select or create a user
        self.logged_in_user = self.select_user() # Store the returned user
        # Load their data
        self.load_user_data()
        # Show the main menu
        self.main_menu()

    def select_user(self):
        """
        Prompts the user to select or create a username.

        :return: The selected User object.
        """
        return self.db.select_user()

    def load_user_data(self):
        """Loads the habits for the current user from the db."""
        # Need new method in UserDatabase

    def main_menu(self):
        """Displays the main menu and handles user navigation."""
        while True:
            print("""\n- - - Main Menu - - -
            1. My Habits
            2. My Analytics
            3. Select a different user
            4. Exit
            """)

            choice = input("Enter your choice (1-4): ").strip()

            if choice == "1":
                self.habits_menu
            elif choice == "2":
                self.analytics_menu
            elif choice == "3":
                self.logged_in_user = self.select_user()
                self.load_user_data()
            elif choice == "4":
                print("Until next time! Stay on track!")
            else:
                print("Sorry, invalid option. Please try again!")


        # I. My habits
        # II. My Analytics
        # III. Select a different user
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
