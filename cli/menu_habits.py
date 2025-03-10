"""
Menu: Habits - Submenu of My Habit Tracker for managing habits
"""
from typing import List

from .menu_habit_detail import menu_habit_detail
from core.habit import Habit
from helpers.helper_functions import reload_cli, reload_menu_countdown, check_exit_cmd


def menu_habits(ht):
    """
    Displays the habits menu and handles user navigation.

    Parameters:
         ht: The HabitTracker instance that manages the application state.
    """
    while True:
        # Clear the screen and display the menu header
        reload_cli()
        print("(Type 'quit' at any time to exit the application)")
        print("""
        - - - My Habits - - -
        
        1. Register a new habit
        2. List all habits
        3. Daily habits
        4. Weekly habits
        5. << Back to My Habit Tracker
        """)

        # Get user choice
        choice = input("\nEnter your choice (1-5): ").strip()

        # Check for exit command
        check_exit_cmd(choice)

        # Handle menu options
        if choice == "1":
            # Register a new habit
            ht.db.new_habit(ht.logged_in_user)

        elif choice == "2":
            # List all habits
            all_habits = ht.analytics.list_all_habits()
            display_habits_and_select(ht, all_habits, "All", None)

        elif choice == "3":
            # Filter and display daily habits
            daily_habits = ht.analytics.list_habits_by_periodicity("daily")
            display_habits_and_select(ht, daily_habits, "Daily", "daily")

        elif choice == "4":
            # Filter and display weekly habits
            weekly_habits = ht.analytics.list_habits_by_periodicity("weekly")
            display_habits_and_select(ht, weekly_habits, "Weekly", "weekly")

        elif choice == "5":
            # Return to My Habit Tracker Menu
            return

        else:
            # Handle invalid input
            print("\nInvalid input. Please try again!")
            reload_menu_countdown()

def display_habits_and_select(ht, habits: List[Habit], display_type: str, set_frequency: str = None) -> None:
    """
    Displays an indexed list of habits and allows the user to select one for detailed view.

    Parameters:
        ht: The HabitTracker instance that manages the application state.
        habits: List of Habit objects to display.
        display_type: Type of habits being displayed ("All", "Daily", "Weekly").
        set_frequency: Pre-set frequency for new habits("Daily", "Weekly", or None).
    """
    # Clear the screen
    reload_cli()

    # Check if there are no habits to display
    if not habits:
        # If no habits, display a message based on the habit type
        # For daily, weekly habits
        if display_type in ["daily", "weekly"]:
            print(f"You don't have any {display_type} habits yet!")
            reload_menu_countdown()
        # For all habits
        else:
            print("You don't have any registered habits yet!")
            reload_menu_countdown()

        # Offer to create a new habit with pre-set frequency/None or return
        while True:
            # If accessed from display daily or weekly habits
            if set_frequency:
                print("(Type 'quit' at any time to exit the application)")
                print(f"""
                Would you like to create a new {set_frequency} habit?

                1. Register a {set_frequency} habit
                2. << Back to My Habits Menu
                """)

                choice = input("\nEnter your choice (1-2): ").strip()

                # Check for exit command
                check_exit_cmd(choice)

                if choice == "1":
                    # Create a new habit with the pre-set frequency
                    ht.db.new_habit(ht.logged_in_user, set_frequency)
                elif choice == "2":
                    # Return to My Habits Menu
                    reload_menu_countdown()
                    return
                else:
                    # Handle invalid input
                    print("\nInvalid input. Please try again!")
                    reload_menu_countdown()

            # If accessed from display all habits
            else:
                print("(Type 'quit' at any time to exit the application)")
                print(f"""
                Would you like to create a new habit?

                1. Register a new habit
                2. << Back to My Habits Menu
                """)

                choice = input("\nEnter your choice (1-2): ").strip()

                # Check for exit command
                check_exit_cmd(choice)

                if choice == "1":
                    # Create a new habit without a pre-set frequency
                    ht.db.new_habit(ht.logged_in_user)
                elif choice == "2":
                    # Return to My Habit Menu
                    reload_menu_countdown()
                    return
                else:
                    # Handle invalid input
                    print("\nInvalid input. Please try again!")
                    reload_menu_countdown()

    # If there are habits to display, show them
    while True:
        reload_cli()
        print("(Type 'quit' at any time to exit the application)")
        print(f"\n- - - {display_type.title()} Habits - - -")

        # Display habits with indexing
        for idx, habit in enumerate(habits, 1):
            # For daily, weekly habits
            if habit.frequency in ["daily", "weekly"]:
                print(f"\n{idx}. {habit.name}")
            # For all habits
            else:
                print(f"\n{idx}. {habit.name} ({habit.frequency})")

        # Add option to return to the previous menu
        back_option = len(habits) + 1
        print(f"\n{back_option}. << Back to My Habits Menu")

        # Get user selection
        choice = input(f"\nEnter your choice (1-{back_option}): ").strip()

        # Check for exit command
        check_exit_cmd(choice)

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
                # Handle invalid int input
                print("\nInvalid choice. Please try again!")
                reload_menu_countdown()
        # Handle invalid str input
        except ValueError:
            print("\nPlease enter a number!")
            reload_menu_countdown()