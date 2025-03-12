"""
Menu: Habit Detail - Submenu of My Habits Menu for managing and analyzing one individual habit
"""
from cli.calendar_view import view_completions_calendar
from cli.menu_analytics import menu_analytics_one_habit
from core.habit import Habit
from db_and_managers.database import Database
from helpers.helper_functions import reload_cli, reload_menu_countdown, check_exit_cmd, exit_msg
from helpers.colors import BLUE, RES, GRAY

# Create a db instance
db = Database()

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
        exit_msg()
        print(f"""
        {BLUE}- - - {habit.name}'s Details - - -{RES}

        1. Complete for today
        2. View calendar and manage completions
        3. Analytics
        4. View creation date
        5. Delete habit
        
        {GRAY}6. << Back to My Habits Menu{RES}
        """)

        # Get user choice
        choice = input("\nEnter your choice (1-6): ").strip()

        # Check for exit command
        check_exit_cmd(choice)

        # Handle menu options
        if choice == "1":
            # Mark the habit as complete for today
            db.complete_habit_today(ht, habit)

        elif choice == "2":
            # View completions on calendar
            view_completions_calendar(ht, habit)

        elif choice == "3":
            # View analytics for the selected habit
            menu_analytics_one_habit(ht, habit)

        elif choice == "4":
            # View the creation date of the habit
            print(f"\nHabit '{habit.name}' was created on: {habit.creation.strftime('%Y-%m-%d')}")
            input("Press ENTER to continue...")

        elif choice == "5":
            # Delete selected habit entirely
            db.delete_habit(ht, habit)

        elif choice == "6":
            # Return to My Habits Menu
            return

        else:
            # Handle invalid input
            print("\nInvalid input! Please try again!")
            reload_menu_countdown()