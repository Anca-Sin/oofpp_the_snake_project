"""
Menu: My Habit Tracker
"""
from cli.menu_analytics import menu_analytics
from cli.menu_habits import menu_habits
from helpers.helper_functions import reload_cli, reload_menu_countdown


def menu_my_habit_tracker(ht):
    """
    Displays the habit tracker menu and handles user navigation.

    :param ht:  The HabitTracker instance.
    """
    while True:
        reload_cli()
        print("""- - - My Habit Tracker
        
        1. My Habits
        2. My Analytics
        3. Back to Main Menu
        """)

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            menu_habits(ht)

        elif choice == "2":
            menu_analytics(ht)

        elif choice == "3":
            return

        else:
            print("\nInvalid input. Please try again!")
            reload_menu_countdown()