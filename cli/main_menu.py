"""
Menu: Main Menu - First menu after application start
"""
import sys
import time

from .menu_my_habit_tracker import my_habit_tracker
from core.analytics import Analytics
from helpers.helper_functions import reload_cli, reload_menu_countdown

def main_menu(ht) -> None:
    """
    Displays the main menu and handles user navigation.

    :param ht: The HabitTracker instance.
    """
    while True:
        reload_cli()
        print("""- - - Main Menu - - -
        
        1. My Habit Tracker
        2. Select a different user
        3. Delete this user
        4. Exit the application
        """)

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            my_habit_tracker(ht)

        elif choice == "2":
            ht.logged_in_user = ht.db.select_user()
            ht.db.load_habits(ht.logged_in_user)
            ht.analytics = Analytics(ht.logged_in_user)

        elif choice == "3":
            ht.db.delete_user()

        elif choice == "4":
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
            print("\nInvalid input. Please try again!")
            reload_menu_countdown()