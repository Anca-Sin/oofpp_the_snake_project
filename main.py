"""
Habit Tracker Application - Main Entry Point

- it initializes the application and starts the main menu
"""

from cli.main_menu import main_menu
from core.analytics import Analytics
from db_and_managers.database import Database
from helpers.helper_functions import reload_cli, wavey_mctrackface


class HabitTracker:
    """
    My baby <3

    - serves at the central coordinator for the entire application
    - interacts with the user through the CLI package modules (menus)

    Attributes:
        db (Database):         Initializes the Database instance.
        logged_in_user (User): The currently selected user (no real "log in" implemented, only selection).
        analytics (Analytics): Initializes the Analytics instance.
    """

    def __init__(self):
        """Initializes the habit tracker."""
        self.db = Database()       # Local SQLite db access
        self.logged_in_user = None # Will be set during user selection
        self.analytics = None      # Will be initialized after user selection

    def start(self):
        """
        Starts the Habit Tracker app.

        - display a welcome header
        - loads existing users from the db, which:
                - prompts to select from existing users or create a new user
                - loads the selected user's habits from the db
        - initializes the analytics for the selected users
        - opens the main menu
        """
        # Wavey greets the user
        reload_cli()
        wavey_mctrackface()

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