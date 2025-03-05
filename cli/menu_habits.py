"""
Menu: Habits - For managing and viewing habits
"""
from core.habit import Habit
from helpers.helper_functions import reload_cli, reload_menu_countdown


def menu_habits(ht):
    """
    Displays the habits menu and handles user navigation.

    :param ht: The HabitTracker instance.
    """
    while True:
        reload_cli()
        print("""- - - My Habits - - -
        
        1. Register a new habit
        2. List all habits
        3. Daily habits
        4. Weekly habits
        5. Back to My Habit Tracker
        """)

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            ht.db.new_habit(ht.logged_in_user)

        elif choice == "2":
            ht.analytics.list_all_habits()

        elif choice == "3":
            ht.analytics.list_habits_by_periodicity("daily")

        elif choice == "4":
            ht.analytics.list_habits_by_periodicity("weekly")

        else:
            print("\nInvalid input. Please try again!")
            reload_menu_countdown()