"""
Habit Details Menu module

Detailed interface for managing one individual habit.
It manages:
- direct completing today
- viewing calendar and managing completions
- viewing individual analytics for the habit
- viewing its creation date
- habit deletion
- going back to My Habits Menu
- app exiting
"""

from cli.calendar_view import view_completions_calendar
from cli.menu_analytics import menu_analytics_one_habit
from core.analytics import Analytics
from core.habit import Habit
from helpers.helper_functions import reload_cli, check_exit_cmd, exit_msg, enter, invalid_input
from helpers.text_formating import BLUE, RES, RED, GREEN


def menu_habit_detail(ht, habit: Habit) -> None:
    """
    The detailed menu of a selected habit.

    Parameters:
        ht: The HabitTracker instance managing app state.
        habit: The selected Habit object to manage.
    """
    while True:
        # Clear the screen and display the menu header
        reload_cli()
        exit_msg(ht.logged_in_user)
        print(f"""
        {BLUE}- - -{RES} {habit.name} {BLUE}Details Menu - - -{RES}

        1 - Complete for today {GREEN}(^_^)/{RES}
        2 - Calendar View & Completion Manager
        3 - Analytics
        4 - View creation date
        5 - {RED}Delete{RES} habit
        
        {enter()} Back to My Habits Menu
        """)

        # Get user choice
        choice = input("        Enter your choice (1-5): ").strip()

        # Check for exit command
        check_exit_cmd(choice)

        # Handle menu options
        if choice == "1":
            # Mark the habit as complete for today
            ht.db.complete_habit_today(ht.logged_in_user, habit)

            # Refreshing Analytics instance
            ht.analytics = Analytics(ht.logged_in_user)

        elif choice == "2":
            # View completions on calendar
            view_completions_calendar(ht, habit)

        elif choice == "3":
            # View analytics for the selected habit
            menu_analytics_one_habit(ht, habit)

        elif choice == "4":
            # View the creation date of the habit
            input(
f"\nHabit '{habit.name}' was put on track on {habit.creation_date}! {enter()} to return..."
            )

        elif choice == "5":
            # Delete selected habit
            ht.db.delete_habit(ht.logged_in_user, habit)

            # Refreshing Analytics instance
            ht.analytics = Analytics(ht.logged_in_user)

            # Go to Menu Habits
            from cli.menu_habits import menu_habits # Avoid circular import
            menu_habits(ht)

        elif choice == "":
            # Return to My Habits Menu
            return

        else:
            # Handle invalid input
            invalid_input()