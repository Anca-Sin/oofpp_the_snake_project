"""
Menu: My Habit Tracker - Second after Main Menu
"""
from cli.menu_analytics import menu_analytics_all_habits
from cli.menu_habits import menu_habits
from helpers.helper_functions import reload_cli, reload_menu_countdown

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
        print("""- - - My Habit Tracker
        
        1. My Habits
        2. My Analytics
        3. Back to Main Menu
        """)

        # Get user choice
        choice = input("\nEnter your choice (1-3): ").strip()

        # Handle menu options
        if choice == "1":
            # Got to Habits Menu for managing habits
            menu_habits(ht)

        elif choice == "2":
            # Go to Analytics Menu across all habits
            menu_analytics_all_habits(ht)

        elif choice == "3":
            # Return to Main Menu
            return

        else:
            # Handle invalid input
            print("\nInvalid input. Please try again!")
            reload_menu_countdown()