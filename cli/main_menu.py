"""
Menu: Main Menu - First menu after application start
"""
import sys
import time

from .menu_my_habit_tracker import menu_my_habit_tracker
from core.analytics import Analytics
from helpers.helper_functions import reload_cli, reload_menu_countdown

def main_menu(ht) -> None:
    """
    Displays the main menu and handles user navigation.

    Args:
        ht: The HabitTracker instance that manages the application state.
    """
    while True:
        # Clear the screen and display the menu header
        reload_cli()
        print("""- - - Main Menu - - -
        
        1. My Habit Tracker
        2. Select a different user
        3. Delete this user
        4. Exit the application
        """)

        # Get user choice
        choice = input("\nEnter your choice (1-4): ").strip()

        # Handle menu options
        if choice == "1":
            # Go to my habit tracker menu
            menu_my_habit_tracker(ht)

        elif choice == "2":
            # Select a different user
            ht.logged_in_user = ht.db.select_user()

            # Load the newly selected user's habits
            ht.db.load_habits(ht.logged_in_user)

            # Create an analytics instance for the newly selected user
            ht.analytics = Analytics(ht.logged_in_user)

        elif choice == "3":
            # Delete the selected user
            ht.db.delete_user(ht.logged_in_user)

        elif choice == "4":
            # Exit the application with a countdown
            print("\nUntil next time! Do your best to stay on track!")
            print("Exiting in...")
            time.sleep(1)
            print("""2
                ...
                """)
            time.sleep(1)
            print("""1
                ...
                """)
            time.sleep(1)
            sys.exit(0)

        else:
            # Handle invalid input
            print("\nInvalid input. Please try again!")
            reload_menu_countdown()