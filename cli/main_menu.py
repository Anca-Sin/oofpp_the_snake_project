"""
Menu: Main Menu - First menu after application start
"""
import sys
import time

from .menu_my_habit_tracker import menu_my_habit_tracker
from core.analytics import Analytics
from helpers.helper_functions import reload_cli, reload_menu_countdown, check_exit_cmd, exit_msg
from helpers.colors import GRAY, RES, BLUE, RED, GREEN


def main_menu(ht) -> None:
    """
    Displays the main menu and handles user navigation.

    Parameters:
        ht: The HabitTracker instance that manages the application state.
    """
    while True:
        # Clear the screen and display the menu header
        reload_cli()
        exit_msg(ht.logged_in_user)
        print(f"""
        {BLUE}- - - Main Menu - - -{RES}
        
        {GREEN}1 - My Habit Tracker{RES}
        2 - {RED}Delete{RES} this user
        
        {GRAY}ENTER << Select a different user{RES} 
        """)

        # Get user choice
        choice = input("\nEnter your choice (1-2): ").strip()

        # Check for exit command
        check_exit_cmd(choice)

        # Handle menu options
        if choice == "1":
            # Go to my habit tracker menu
            menu_my_habit_tracker(ht)

        elif choice == "":
            # Select a different user
            ht.logged_in_user = ht.db.select_user()

            # Recreating a fresh Analytics instance
            ht.analytics = Analytics(ht.logged_in_user, ht.db)

        elif choice == "2":
            # Delete the selected user
            ht.db.delete_user(ht.logged_in_user)

            # Recreating a fresh Analytics instance
            ht.analytics = Analytics(ht.logged_in_user, ht.db)

        else:
            # Handle invalid input
            print("\nInvalid input. Please try again!")
            reload_menu_countdown()