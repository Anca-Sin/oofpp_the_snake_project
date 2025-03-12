"""
Menu: My Habit Tracker - Second after Main Menu
"""
from cli.menu_analytics import menu_analytics_all_habits
from cli.menu_habits import menu_habits
from helpers.helper_functions import reload_cli, reload_menu_countdown, check_exit_cmd, exit_msg
from helpers.colors import BLUE, RES, GRAY


def menu_my_habit_tracker(ht):
    """
    Displays the habit tracker menu and handles user navigation.

    - redirects to habits manager (create, view, complete, delete)
    - redirects to viewing analytics across all habits
    - can go back to main menu

    Parameters:
        ht: The HabitTracker instance that manages the application state.
    """
    while True:
        # Clear the screen and display the menu header
        reload_cli()
        exit_msg(ht.logged_in_user)
        print(f"""
        {BLUE}- - - My Habit Tracker - - -{RES}
        
        1 - My Habits
        2 - My Analytics
        
        {GRAY}ENTER << Back to Main Menu{RES}
        """)

        # Get user choice
        choice = input("\nEnter your choice (1-2): ").strip()

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
            print("\nInvalid input. Please try again!")
            reload_menu_countdown()