"""
Menu: Analytics - For viewing statistics on one habit or across all habits

menu_analytics_one_habit: Submenu of Habit Details Menu
menu_analytics_all_habits: Submenu of My Habit Tracker Menu
"""
from core.habit import Habit
from helpers.helper_functions import reload_cli, reload_menu_countdown, check_exit_cmd, exit_msg
from helpers.colors import BLUE, RES, RED, GRAY


def menu_analytics_one_habit(ht, habit: Habit) -> None:
    """
    Displays the Analytics Menu for a selected habit.

    Parameters:
        ht: The HabitTracker instance that manages the application state.
        habit: The selected Habit object to analyze.
    """
    # Get the Analytics instance from the HabitTracker
    analytics = ht.analytics

    # Clear the screen and display the menu header
    reload_cli()
    exit_msg(ht.logged_in_user)

    print(f"\n{BLUE}        - - - {habit.name}'s Analytics - - -{RES}")
    print(f"\n        >> Current streak:     {RED} {habit.streaks.current_streak}{RES}")
    print(f"        >> Longest streak:       {RED} {analytics.longest_streak_for_habit(habit.name)}{RES}")
    print(f"        >> Average streak length:{RED} {round(analytics.average_streak_length_habit(habit.name), 2)}{RES}")
    input(f"\n{GRAY}<< ENTER to go << Back to {habit.name}'s Detail Menu...{RES}")
    return

def menu_analytics_all_habits(ht) -> None:
    """
    Displays the general Analytics Menu.

    Parameters:
        ht: The HabitTracker instance that manages the application state.
    """

    while True:
        # Clear the screen and display the menu header
        reload_cli()
        exit_msg(ht.logged_in_user)
        print(f"""
        {BLUE}- - - My Analytics - - -{RES}
        
        1 - [All Habits]
        2 - [Daily - Weekly]
        
        {GRAY}ENTER << Back to My Habit Tracker Menu{RES}
        """)

        # Check if the user has any habits to analyze
        if not ht.logged_in_user.habits:
            # If no habits exist, inform the user and prompt for return
            print("""\nYou don't have any habits yet!
            
            Navigate to 'My Habit Tracker' -> 'My Habits' to register a new habit!""")
            input(f"{GRAY}ENTER << to return...{RES} ")
            # Return to My Habit Tracker Menu
            return

        # If user has registered habits continue to prompt for choice
        else:
            # Get user choice
            choice = input("\nEnter your choice (1-2): ").strip()

            # Check for exit command
            check_exit_cmd(choice)

            if choice == "1":
                submenu1_analytics_all_habits(ht)
            elif choice == "2":
                submenu2_analytics_d_w_habits(ht)
            elif choice == "":
                from cli.menu_my_habit_tracker import menu_my_habit_tracker # Avoid circular import
                menu_my_habit_tracker(ht)
            else:
                # Handle invalid input
                print("\nInvalid input. Please try again!")
                reload_menu_countdown()

def submenu1_analytics_all_habits(ht):
    """Displays the Analytics across all habits."""
    # Get the Analytics instance from the HabitTracker
    analytics = ht.analytics

    while True:
        # Clear the screen and display the menu header
        reload_cli()
        exit_msg(ht.logged_in_user)
        print(f"\n{BLUE}        - - - [All Habits] Analytics - - -{RES}")
        habit_name, streak = analytics.longest_streak_all_habits()
        print(f"\n{GRAY}        >> Longest streak:{RES}        '{RED}{habit_name}{RES}' with a {RED}{streak}{RES}-days streak")
        habit_name, count = analytics.most_completed_habit()
        print(f"{GRAY}        >> Most completed habit:{RES}  '{RED}{habit_name}{RES}' with {RED}{count}{RES} completions")
        habit_name, count = analytics.least_completed_habit()
        print(f"{GRAY}        >> Least completed habit:{RES} '{RED}{habit_name}{RES}' with {RED}{count}{RES} completions")
        avg_streak = round(analytics.average_streak_all_habits(), 2)
        print(f"{GRAY}        >> Average streak length:{RES}  {RED}{round(analytics.average_streak_all_habits(), 2)}{RES}")
        i = input(f"\n{GRAY}ENTER << Back to My Analytics Menu...{RES}")

        # Check for exit command
        check_exit_cmd(i)

        return

def submenu2_analytics_d_w_habits(ht):
    """Displays the Analytics for all daily and weekly habits."""
    # Get the Analytics instance from the HabitTracker
    analytics = ht.analytics

    while True:
        # Clear the screen and display the menu header
        reload_cli()
        exit_msg(ht.logged_in_user)
        print(f"\n{BLUE}        - - - [Daily - Weekly] Analytics - - -{RES}")

        print(f"{GRAY}\n        >> Longest streak{RES}")
        daily_name, daily_streak = analytics.longest_streak_by_periodicity("daily")
        print(f"        {GRAY}Daily:{RES}  '{RED}{daily_name}{RES}' with a {RED}{daily_streak}{RES}-day streak")
        weekly_name, weekly_streak = analytics.longest_streak_by_periodicity("weekly")
        print(f"        {GRAY}Weekly:{RES} '{RED}{weekly_name}{RES}' with a {RED}{weekly_streak}{RES}-day streak")

        print(f"\n{GRAY}        >> Most completed habits{RES}")
        daily_name, daily_count = analytics.most_completed_by_periodicity("daily")
        print(f"        {GRAY}Daily:{RES}  '{RED}{daily_name}{RES}' with {RED}{daily_count}{RES} completions")
        weekly_name, weekly_count = analytics.most_completed_by_periodicity("weekly")
        print(f"        {GRAY}Weekly:{RES} '{RED}{weekly_name}{RES}' with {RED}{weekly_count}{RES} completions")

        print(f"\n{GRAY}        >> Least completed habits{RES}")
        daily_name, daily_count = analytics.least_completed_by_periodicity("daily")
        print(f"        {GRAY}Daily:{RES}  '{RED}{daily_name}'{RES} with {RED}{daily_count}{RES} completions <<")
        weekly_name, weekly_count = analytics.least_completed_by_periodicity("weekly")
        print(f"        {GRAY}Weekly:{RES} '{RED}{weekly_name}'{RES} with {RED}{weekly_count}{RES} completions <<")

        print(f"\n{GRAY}        >> Average streak length{RES}")
        avg_daily = round(analytics.average_streak_by_periodicity("daily"), 2)
        print(f"        {GRAY}Daily:{RES}   {RED}{avg_daily}{RES}")
        avg_weekly = round(analytics.average_streak_by_periodicity("weekly"))
        print(f"        {GRAY}Weekly:{RES}  {RED}{avg_weekly}{RES}")

        i = input(f"\n{GRAY}ENTER << Back to My Analytics Menu...{RES}")

        # Check for exit command
        check_exit_cmd(i)

        return