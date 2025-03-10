"""
Menu: Main Menu - First menu after application start
"""
import sys
import time

from .menu_my_habit_tracker import menu_my_habit_tracker
from core.analytics import Analytics
from helpers.helper_functions import reload_cli, reload_menu_countdown, check_exit_cmd


def main_menu(ht) -> None:
    """
    Displays the main menu and handles user navigation.

    Parameters:
        ht: The HabitTracker instance that manages the application state.
    """
    while True:
        # Clear the screen and display the menu header
        reload_cli()
        print("(Type 'quit' at any time to exit the application)")
        print("""
        - - - Main Menu - - -
        
        1. My Habit Tracker
        2. Select a different user
        3. Delete this user
        """)

        # Get user choice
        choice = input("\nEnter your choice (1-3): ").strip()

        # Check for exit command
        check_exit_cmd(choice)

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

        else:
            # Handle invalid input
            print("\nInvalid input. Please try again!")
            reload_menu_countdown()