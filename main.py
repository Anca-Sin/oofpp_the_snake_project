"""
Habit Tracker Application - Main Entry Point

- it initializes the application and starts the main menu
"""

from cli.main_menu import main_menu
from core.analytics import Analytics
from db_and_managers.database import Database

class HabitTracker:
    """
    Main class to manage users, habit creation, streaks, and analytics.

    - serves at the central coordinator for the entire application
    - it initializes the db
    - manages user selection
    - provides access to habit analytics functionality

    Attributes:
        db (Database): Instance of the Database for managing user and habit data
        logged_in_user (User): The currently selected user (no real "log in" implemented, only selection)
        analytics (Analytics): Analytics functionality for the user.
    """

    def __init__(self):
        """Initializes the habit tracker."""
        self.db = Database()       # Local SQLite db access
        self.logged_in_user = None # Will be set during user selection
        self.analytics = None      # Will be initialized after user selection

    def start(self):
        """
        Starts the Habit Tracker app.

        - display a welcome message
        - loads existing users from the db
        - prompts to select from existing users or create a new user
        - loads the selected user's habits from the db
        - initializes the analytics for the selected users
        - opens the main menu

        - no db connection needed, each Database method handles its own connection
        """
        print("        Welcome to your - - -  Habit Tracker- - -")

        # Select an existing user or create a new one
        # Habits are loaded internally in the database method
        self.logged_in_user = self.db.select_user()

        # Creating the first Analytics instance
        self.analytics = Analytics(self.logged_in_user)

        # Show the main menu to start user interaction
        main_menu(self)

if __name__ == "__main__":
    # Create and start the habit tracker
    tracker = HabitTracker()
    tracker.start()