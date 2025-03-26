"""
Menu: Habit Detail - Submenu of My Habits Menu for managing and analyzing one individual habit
"""
from cli.calendar_view import view_completions_calendar
from cli.menu_analytics import menu_analytics_one_habit
from core.analytics import Analytics
from core.habit import Habit
from db_and_managers.database import Database
from helpers.helper_functions import reload_cli, reload_menu_countdown, check_exit_cmd, exit_msg
from helpers.text_formating import BLUE, RES, GRAY, RED

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
        exit_msg(ht.logged_in_user)
        print(f"""
        {BLUE}- - - '{habit.name}' Details Menu - - -{RES}

        1 - Complete for today
        2 - Calendar and manage completions
        3 - Analytics
        4 - View creation date
        5 - {RED}Delete{RES} habit
        
        {GRAY}ENTER << Back to My Habits Menu{RES}
        """)

        # Get user choice
        choice = input("\nEnter your choice (1-5): ").strip()

        # Check for exit command
        check_exit_cmd(choice)

        # Handle menu options
        if choice == "1":
            # Mark the habit as complete for today
            ht.db.complete_habit_today(ht.logged_in_user, habit)

            # Recreating a fresh Analytics instance
            ht.analytics = Analytics(ht.logged_in_user)

        elif choice == "2":
            # View completions on calendar
            view_completions_calendar(ht, habit)

        elif choice == "3":
            # View analytics for the selected habit
            menu_analytics_one_habit(ht, habit)

        elif choice == "4":
            # View the creation date of the habit
            print(f"\nHabit '{habit.name}' was created on: {habit.creation_date.strftime('%Y-%m-%d')}")
            input(f"{GRAY}ENTER << to continue...{RES}")

        elif choice == "5":
            # Delete selected habit entirely
            ht.db.delete_habit(ht.logged_in_user, habit)

            # Recreating a fresh Analytics instance
            ht.analytics = Analytics(ht.logged_in_user)

            # Go to Menu Habits
            from cli.menu_habits import menu_habits # Avoid circular import
            menu_habits(ht)

        elif choice == "":
            # Return to My Habits Menu
            return

        else:
            # Handle invalid input
            print("\nInvalid input! Please try again!")
            reload_menu_countdown()