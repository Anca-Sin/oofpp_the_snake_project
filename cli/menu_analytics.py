"""
Analytics module containing 2 menus for:
- One habit analytics:         submenu of Habit Details Menu
- Analytics across all habits: submenu of My Habit Tracker Menu
- deploys all Analytics class methods except listings
"""

from core.habit import Habit
from helpers.helper_functions import reload_cli, reload_menu_countdown, check_exit_cmd, exit_msg, enter, invalid_input
from helpers.text_formating import BLUE, RES, RED, GRAY, GREEN

def menu_analytics_one_habit(ht, habit: Habit) -> None:
    """
    The Analytics Menu for a selected habit.

    Args:
        ht: The HabitTracker instance managing app state.
        habit: The selected Habit object to analyze.
    """
    # Access HabitTracker's Analytics instance
    analytics = ht.analytics

    # Clear the screen and display the menu header
    reload_cli()
    print("")
    print(f"{GRAY}Logged in as:{RES} {GREEN}{ht.logged_in_user.username}{RES}")

    print(f"\n{BLUE}        - - - '{habit.name}' Analytics - - -{RES}")
    print(f"\n        {GRAY}>> {RES}Current streak:     {RED}   {habit.streaks.current_streak}{RES}-days streak")
    print(f"        {GRAY}>> {RES}Longest streak:       {RED} {analytics.longest_streak_for_habit(habit.name)}{RES}-days streak")
    print(f"        {GRAY}>> {RES}Average streak length:{RED} {round(analytics.average_streak_length_habit(habit.name), 2)}{RES} days")

    input(f"\n        {enter()} Back to '{habit.name}' Details Menu...")
    return

def menu_analytics_all_habits(ht) -> None:
    """
    The Analytics menu across all habits.

    Args:
        ht: The HabitTracker instance managing app state.
    """
    while True:
        # Clear the screen and display the menu header
        reload_cli()
        exit_msg(ht.logged_in_user)
        print(f"""
        {BLUE}- - - My Analytics - - -{RES}
        
        1 - [All Habits]
        2 - [Daily - Weekly]
        
        {enter()} to My Habit Tracker Menu
        """)

        # Check if the user has any habits to analyze
        if not ht.logged_in_user.habits:
            # If no habits exist, inform the user and prompt for return
            input(f"""
            You don't have any habits yet!
            
            Navigate to 'My Habit Tracker' -> 'My Habits' to register a new habit! {enter()} to return...""")
            # Return to My Habit Tracker Menu
            return

        # If user has registered habits continue to prompt for choice
        else:
            # Get user choice
            choice = input("\n        Enter your choice (1-2): ").strip()

            # Check for exit command
            check_exit_cmd(choice)

            if choice == "1":
                _analytics_all_habits(ht)
            elif choice == "2":
                _analytics_d_w_habits(ht)
            elif choice == "":
                return
            else:
                # Handle invalid input
                invalid_input()
                reload_menu_countdown()

def _analytics_all_habits(ht):
    """Analytics display across all habits."""
    # Access HabitTracker's Analytics instance
    analytics = ht.analytics

    while True:
        # Clear the screen and display the menu header
        reload_cli()
        print("")
        print(f"{GRAY}Logged in as:{RES} {GREEN}{ht.logged_in_user.username}{RES}")
        print(f"\n{BLUE}        - - - [All Habits] Analytics - - -{RES}")
        habit_name, streak = analytics.longest_streak_all_habits()
        print(f"\n{GRAY}        >>{RES} Longest streak:        '{RED}{habit_name}{RES}' with a {RED}{streak}{RES}-days streak")
        habit_name, count = analytics.most_completed_habit()
        print(f"{GRAY}        >>{RES} Most completed habit:  '{RED}{habit_name}{RES}' with {RED}{count}{RES} completions")
        habit_name, count = analytics.least_completed_habit()
        print(f"{GRAY}        >>{RES} Least completed habit: '{RED}{habit_name}{RES}' with {RED}{count}{RES} completions")
        print(f"{GRAY}        >>{RES} Average streak length:  {RED}{round(analytics.average_streak_all_habits(), 2)}{RES} days")

        input(f"\n        {enter()} Back to My Analytics Menu...")
        return

def _analytics_d_w_habits(ht):
    """Analytics display sorted by daily and weekly habits."""
    # Access HabitTracker's Analytics instance
    analytics = ht.analytics

    while True:
        # Clear the screen and display the menu header
        reload_cli()
        print("")
        print(f"{GRAY}Logged in as:{RES} {GREEN}{ht.logged_in_user.username}{RES}")
        print(f"\n{BLUE}        - - - [Daily - Weekly] Analytics - - -{RES}")

        print(f"{GRAY}\n        >>{RES} Longest streak")
        daily_name, daily_streak = analytics.longest_streak_by_periodicity("daily")
        print(f"        {GRAY}Daily:{RES}  '{RED}{daily_name}{RES}' with a {RED}{daily_streak}{RES}-day streak")
        weekly_name, weekly_streak = analytics.longest_streak_by_periodicity("weekly")
        print(f"        {GRAY}Weekly:{RES} '{RED}{weekly_name}{RES}' with a {RED}{weekly_streak}{RES}-day streak")

        print(f"\n{GRAY}        >>{RES} Most completed habits")
        daily_name, daily_count = analytics.most_completed_by_periodicity("daily")
        print(f"        {GRAY}Daily:{RES}  '{RED}{daily_name}{RES}' with {RED}{daily_count}{RES} completions")
        weekly_name, weekly_count = analytics.most_completed_by_periodicity("weekly")
        print(f"        {GRAY}Weekly:{RES} '{RED}{weekly_name}{RES}' with {RED}{weekly_count}{RES} completions")

        print(f"\n{GRAY}        >>{RES} Least completed habits")
        daily_name, daily_count = analytics.least_completed_by_periodicity("daily")
        print(f"        {GRAY}Daily:{RES}  '{RED}{daily_name}'{RES} with {RED}{daily_count}{RES} completions <<")
        weekly_name, weekly_count = analytics.least_completed_by_periodicity("weekly")
        print(f"        {GRAY}Weekly:{RES} '{RED}{weekly_name}'{RES} with {RED}{weekly_count}{RES} completions <<")

        print(f"\n{GRAY}        >>{RES} Average streak length")
        avg_daily = round(analytics.average_streak_by_periodicity("daily"), 2)
        print(f"        {GRAY}Daily:{RES}   {RED}{avg_daily}{RES} days")
        avg_weekly = round(analytics.average_streak_by_periodicity("weekly"))
        print(f"        {GRAY}Weekly:{RES}  {RED}{avg_weekly}{RES} days")

        input(f"\n        {enter()} Back to My Analytics Menu...")
        return