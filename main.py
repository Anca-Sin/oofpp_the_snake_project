"""
Habit Tracker Application - Main Entry Point
"""
from cli.main_menu import main_menu
from core.analytics import Analytics
from db_and_managers.database import Database

class HabitTracker:
    """Main class to manage users, habit creation, streaks, and analytics."""

    def __init__(self):
        """
        Initializes the habit tracker.
        - Connects to the Database (handles storage and retrieval)
        - Optionally handles multiple users, but no login required
        """
        self.db = Database         # Interacts with the local SQLite DB
        self.logged_in_user = None # Currently selected user
        self.analytics = None      # Will be initialized after user selection

    def start(self):
        """
        Starts the Habit Tracker app.
        - Greets the user and allows username selection
        - After selection, loads user data and displays the main menu.
        """
        print("Welcome to your Habit Tracker!")

        # No db connection needed
        # Each db function handles its own connection

        # Select or create a user
        # Will always return a valid user
        self.logged_in_user = self.db.select_user()

        # Load user habits and analytics after selection
        self.db.load_habits(self.logged_in_user)
        self.analytics = Analytics(self.logged_in_user)

        # Show the main menu
        main_menu(self)

if __name__ == "__main__":
    # Create and start the habit tracker
    tracker = HabitTracker()
    tracker.start()