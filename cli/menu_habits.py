"""
My Habits Menu module.

Main interface menu for habit management functionality.
It manages:
- creating new habits
- viewing all habits or sorted by periodicity through the Analytics class
- habit selection from the lists for individual view
- redirects to habit creation when no habits exist
- going back to My Habit Tracker Menu
- app exiting
"""
import time
from typing import List

from core.analytics import Analytics
from .menu_habit_detail import menu_habit_detail
from core.habit import Habit
from helpers.helper_functions import reload_cli, check_exit_cmd, exit_msg, enter, invalid_input
from helpers.text_formating import BLUE, RES, GRAY, GREEN

def menu_habits(ht):
    """
    The user's habits menu.

    Args:
         ht: The HabitTracker instance managing app state.
    """

    while True:
        # Clear the screen and display the menu header
        reload_cli()
        exit_msg(ht.logged_in_user)
        print(f"""
        {BLUE}- - - My Habits - - -{RES}
        
        1 - All my habits
        2 - My daily habits
        3 - My weekly habits
        4 - {GREEN}New{RES} habit
        
        {enter()} Back to My Habit Tracker
        """)

        # Get user choice
        choice = input("        Enter your choice (1-4): ").strip()

        # Check for exit command
        check_exit_cmd(choice)

        # Handle menu options
        if choice == "1":
            # List all habits
            all_habits = ht.analytics.list_all_habits()
            display_habits_and_select(ht, all_habits, "All", None)

        elif choice == "2":
            # Filter and display daily habits
            daily_habits = ht.analytics.list_habits_by_periodicity("daily")
            display_habits_and_select(ht, daily_habits, "Daily", "daily")

        elif choice == "3":
            # Filter and display weekly habits
            weekly_habits = ht.analytics.list_habits_by_periodicity("weekly")
            display_habits_and_select(ht, weekly_habits, "Weekly", "weekly")

        elif choice == "4":
            reload_cli()
            print()
            print(f"{GRAY}Logged in as:{RES} {GREEN}{ht.logged_in_user.username}{RES}")
            print(f"""
        {BLUE}- - - New Habit Setup - - -{RES}
            """)
            # Register a new habit
            ht.db.new_habit(ht.logged_in_user)

            # Refreshing Analytics instance
            ht.analytics = Analytics(ht.logged_in_user)

        elif choice == "":
            # Return to My Habit Tracker Menu
            return

        else:
            # Handle invalid input
            invalid_input()

def display_habits_and_select(ht, habits: List[Habit], display_type: str, set_frequency: str = None) -> None:
    """
    Displays an indexed list of habits and allows the user to select one for detailed view.

    Args:
        ht:            The HabitTracker instance managing app state.
        habits:        List of Habit objects to display.
        display_type:  Type of habits being displayed ("All", "Daily", "Weekly").
        set_frequency: Pre-set frequency for new habits("Daily", "Weekly", or None).
    """
    # Check if there are no habits to display
    if not habits:
        # If no habits, display a message based on the habit type
        # For daily, weekly habits
        if set_frequency in ["daily", "weekly"]:
            print(f"\n{GRAY}You don't have any {RES}{display_type.lower()} {GRAY}habits yet!")
            time.sleep(1)
            print(f"\nRedirecting{RES}...")
            time.sleep(1)
        # For all habits
        else:
            print(f"\n{GRAY}You don't have any registered habits yet!")
            time.sleep(1)
            print(f"\nRedirecting{RES}...")
            time.sleep(1)

        # Offer to create a new habit with pre-set frequency/None or return
        while True:
            # Clear the screen
            reload_cli()
            print()
            print(f"{GRAY}Logged in as:{RES} {GREEN}{ht.logged_in_user.username}{RES}")
            # If accessed from display daily or weekly habits
            if set_frequency:
                print(f"""
        {BLUE}- - - New Habit Setup - - -{RES}

        {GRAY}- frequency automatically set to: {RES}{set_frequency}
                """)
                # Create a new habit with the pre-set frequency
                ht.db.new_habit(ht.logged_in_user, set_frequency)

                # Refreshing Analytics instance
                ht.analytics = Analytics(ht.logged_in_user)
                return

            # If accessed from display all habits
            else:
                print(f"""
                {BLUE}- - - New Habit Setup - - -{RES}
                """)
                # Create a new habit
                ht.db.new_habit(ht.logged_in_user)

                # Refreshing Analytics instance
                ht.analytics = Analytics(ht.logged_in_user)
                return

    # If there are habits to display, show them
    while True:
        reload_cli()
        exit_msg(ht.logged_in_user)
        print(f"""
        {BLUE}- - - '{display_type.title()}' Habits - - -{RES}
        """)

        # Display habits with indexing
        for idx, habit in enumerate(habits, 1):
            # For daily, weekly habits
            if habit.frequency in ["daily", "weekly"]:
                print(f"        {idx} - {habit.name}")
            # For all habits
            else:
                print(f"        {idx} - {habit.name} ({habit.frequency})")

        print(f"\n        {enter()} Back to My Habits Menu")

        # Get user selection
        choice = input(f"\n        Enter your choice (1-{len(habits)}): ").strip()

        # Check for exit command
        check_exit_cmd(choice)

        try:
            if choice == "":
                return

            elif 1 <= int(choice) <= len(habits):
                # Get the selected habit
                selected_habit = habits[int(choice) - 1]
                # Open detail menu for selected habit
                menu_habit_detail(ht, selected_habit)
                return # Return the user to the My Habits Menu after he views the habit details

            else:
                # Handle invalid int input
                invalid_input()

        except ValueError:
            # Handle invalid str input
            invalid_input()