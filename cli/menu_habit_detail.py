"""
Menu: Habit Detail - Submenu of My Habits Menu for managing and analyzing one individual habit
"""
from cli.menu_analytics import menu_analytics_one_habit
from core.habit import Habit
from db_and_managers.manager_completion_db import complete_habit_today, complete_habit_past, delete_completion
from db_and_managers.manager_habit_db import delete_habit
from helpers.helper_functions import reload_cli, reload_menu_countdown, check_exit_cmd


def menu_habit_detail(ht, habit: Habit) -> None:
    """
    Shows a detailed menu for the selected habit.

    Parameters:
        ht: The HabitTracker instance that manages the application state.
        habit: The selected Habit object to manage.
    """
    while True:
        # Clear the screen and display the menu header
        reload_cli()
        print("(Type 'quit' at any time to exit the application)")
        print(f"""
        - - - {habit.name}'s Details - - -

        1. Complete for today
        2. Complete for past date
        3. Delete a completion
        4. Analytics
        5. View creation date
        6. Delete habit
        7. << Back to My Habits Menu
        """)

        # Get user choice
        choice = input("\nEnter your choice (1-7): ").strip()

        # Check for exit command
        check_exit_cmd(choice)

        # Handle menu options
        if choice == "1":
            # Mark the habit as complete for today
            complete_habit_today(ht.logged_in_user, habit)

        elif choice == "2":
            # Mark the habit as complete for a past date
            complete_habit_past(ht.logged_in_user, habit)

        elif choice == "3":
            # Delete a completion
            delete_completion(ht.logged_in_user, habit)

        elif choice == "4":
            # View analytics for the selected habit
            menu_analytics_one_habit(ht, habit)

        elif choice == "5":
            # View the creation date of the habit
            print(f"\nHabit '{habit.name}' was created on: {habit.creation.strftime('%Y-%m-%d')}")
            input("Press ENTER to continue...")

        elif choice == "6":
            # Delete selected habit entirely
            delete_habit(ht.logged_in_user, habit)

        elif choice == "7":
            # Return to My Habits Menu
            return

        else:
            # Handle invalid input
            print("\nInvalid input! Please try again!")
            reload_menu_countdown()