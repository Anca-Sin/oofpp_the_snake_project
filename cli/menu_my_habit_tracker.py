"""
My Habit Tracker Menu module.

Central menu interface after user selection.
It manages:
- access to habit management
- access to analytics across all habits
- going back to Main Menu
- app exiting
"""

from cli.menu_analytics import menu_analytics_all_habits
from cli.menu_habits import menu_habits
from helpers.helper_functions import reload_cli, check_exit_cmd, exit_msg, enter, invalid_input
from helpers.text_formating import BLUE, RES

def menu_my_habit_tracker(ht):
    """
    The habit tracker menu.

    Args:
        ht: The HabitTracker instance managing app state.
    """
    while True:
        # Clear the screen and display the menu header
        reload_cli()
        exit_msg(ht.logged_in_user)
        print(f"""
        {BLUE}- - - My Habit Tracker - - -{RES}
        
        1 - My Habits
        2 - My Analytics
        
        {enter()} Back to Main Menu
        """)

        # Get user choice
        choice = input("        Enter your choice (1-2): ").strip()

        # Check for exit command
        check_exit_cmd(choice)

        # Handle menu options
        if choice == "1":
            # Got to Habits Menu for managing habits
            menu_habits(ht)

        elif choice == "2":
            # Go to Analytics Menu across all habits
            menu_analytics_all_habits(ht)

        elif choice == "":
            # Return to Main Menu
            return

        else:
            # Handle invalid input
            invalid_input()