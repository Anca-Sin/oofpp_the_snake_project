"""
Menu: Habit Detail - For managing and analyzing one individual habit
"""
from cli.menu_analytics import menu_analytics
from core.habit import Habit
from db_and_managers.manager_completion_db import complete_habit_today, complete_habit_past, delete_completion
from db_and_managers.manager_habit_db import delete_habit
from helpers.helper_functions import reload_cli, reload_menu_countdown


def menu_habit_detail(ht, habit: Habit) -> None:
    """
    Shows detailed menu for a selected habit.

    :param ht: The HabitTracker instance.
    :param habit: The selected Habit object.
    """
    while True:
        reload_cli()
        print(f"""- - - {habit.name}'s Details - - -

        1. Complete for today
        2. Complete for past date
        3. Delete a completion
        4. Analytics
        5. Delete habit
        6. Return to My Habits Menu
        """)

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            complete_habit_today(ht.logged_in_user, habit)

        elif choice == "2":
            complete_habit_past(ht.logged_in_user, habit)

        elif choice == "3":
            delete_completion(ht.logged_in_user, habit)

        elif choice == "4":
            menu_analytics(ht, habit)

        elif choice == "5":
            delete_habit(ht.logged_in_user, habit)

        elif choice == "6":
            return

        else:
            print("\nInvalid input! Please try again!")
            reload_menu_countdown()