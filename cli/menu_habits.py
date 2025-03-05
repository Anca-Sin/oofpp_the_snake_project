"""
Menu: Habits - For managing and viewing habits
"""
from typing import List

from .menu_habit_detail import menu_habit_detail
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
            all_habits = ht.analytics.list_all_habits()
            display_habits_and_select(ht, all_habits, "All", None)

        elif choice == "3":
            daily_habits = ht.analytics.list_habits_by_periodicity("daily")
            display_habits_and_select(ht, daily_habits, "Daily", "daily")

        elif choice == "4":
            weekly_habits = ht.analytics.list_habits_by_periodicity("weekly")
            display_habits_and_select(ht, weekly_habits, "Weekly", "weekly")

        elif choice == "5":
            return # Return to My Habit Tracker Menu

        else:
            print("\nInvalid input. Please try again!")
            reload_menu_countdown()

def display_habits_and_select(ht, habits: List[Habit], display_type: str, set_frequency: str = None) -> None:
    """
    Displays an indexed list of habits and allows the user to select one for detailed view or return.

    :param ht: The HabitTracker instance.
    :param habits: List of Habit objects to display.
    :param display_type: Type of habits being displayed (All, Daily, Weekly).
    :param set_frequency: Pre-set frequency for new habits(Daily, Weekly, or None).
    """
    reload_cli()
    if not habits:
        if display_type in ["daily", "weekly"]:
            print(f"You don't have any {display_type} habits yet!")
        else:
            print("You don't have any registered habits yet!")

        # Offer to create a new habit with pre-set frequency/None or return
        while True:
            if set_frequency:
                print(f"""\nWould you like to create a new {set_frequency} habit?

                1. Register a {set_frequency} habit
                2. Return to My Habits Menu
                """)

                choice = input("\nEnter your choice (1-2): ").strip()
                if choice == "1":
                    ht.db.new_habit(ht.logged_in_user, set_frequency)
                elif choice == "2":
                    reload_menu_countdown()
                    return
                else:
                    print("\nInvalid input. Please try again!")
                    reload_menu_countdown()

    while True:
        reload_cli()
        print(f"- - - {display_type.title()} Habits - - -")

        # Display habits with numbering
        for idx, habit in enumerate(habits, 1):
            if habit.frequency in ["daily", "weekly"]:
                print(f"{idx}. {habit.name}")
            else:
                print(f"{idx}. {habit.name} ({habit.frequency})")

        # Add option to return to the previous menu
        back_option = len(habits) + 1
        print(f"{back_option}. Back to My Habits Menu")

        # Get user selection
        choice = input(f"\nEnter your choice (1-{back_option}): ").strip()

        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(habits):
                # Get the selected habit
                selected_habit = habits[choice_num - 1]
                # Open detail menu for selected habit
                menu_habit_detail(ht, selected_habit)
                return # Return the user to the My Habits Menu after he views the habit details
            elif choice_num == back_option:
                return
            else:
                print("\nInvalid choice. Please try again!")
                reload_menu_countdown()
        except ValueError: # Handle string inputs
            print("\nPlease enter a number!")
            reload_menu_countdown()
