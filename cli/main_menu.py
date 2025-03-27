"""
Main Menu module.

Provides the first menu interface for the app = entry point after app start.
It manages:
- navigation to habit tracker functionality
- user deletion
- user switching
- app exiting
"""

from .menu_my_habit_tracker import menu_my_habit_tracker
from core.analytics import Analytics
from helpers.helper_functions import reload_cli, reload_menu_countdown, check_exit_cmd, exit_msg, invalid_input, enter
from helpers.text_formating import RES, BLUE, RED

def main_menu(ht) -> None:
    """
    The main menu of the habit tracker.

    Args:
        ht: The HabitTracker instance managing app state.
    """
    while True:
        # Clear the screen and display the menu header
        reload_cli()
        exit_msg(ht.logged_in_user)
        print(f"""
        {BLUE}- - - Main Menu - - -{RES}
        
        1 - My Habit Tracker
        2 - {RED}Delete{RES} this user
        
        {enter()} Select a different user 
        """)

        # Get user choice
        choice = input("        Enter your choice (1-2): ").strip()

        # Check for exit command
        check_exit_cmd(choice)

        # Handle menu options
        if choice == "1":
            # Go to my habit tracker menu
            menu_my_habit_tracker(ht)

        elif choice == "":
            # Select a different user
            ht.logged_in_user = ht.db.select_user()

            # Refreshing Analytics instance
            ht.analytics = Analytics(ht.logged_in_user)

        elif choice == "2":
            # Delete the selected user
            ht.db.delete_user(ht.logged_in_user)

            # Refreshing Analytics instance
            ht.analytics = Analytics(ht.logged_in_user)

        else:
            # Handle invalid input
            invalid_input()
            reload_menu_countdown()