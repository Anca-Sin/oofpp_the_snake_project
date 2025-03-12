"""
Menu: Analytics - For viewing statistics on one habit or across all habits

menu_analytics_one_habit: Submenu of Habit Details Menu
menu_analytics_all_habits: Submenu of My Habit Tracker Menu
"""
from core.habit import Habit
from helpers.helper_functions import reload_cli, reload_menu_countdown, check_exit_cmd


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

    print("(Type 'quit' at any time to exit the application)")
    print(f"\n        - - - {habit.name}'s Analytics - - -")
    print(f"        >> Current streak: {habit.streaks.current_streak}")
    print(f"        >> Longest streak: {analytics.longest_streak_for_habit(habit.name)}")
    print(f"        >> Average streak length: {round(analytics.average_streak_length_habit(habit.name), 2)}")
    input(f"\nPress ENTER to go << Back to {habit.name}'s Detail Menu...")
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
        print("(Type 'quit' at any time to exit the application)")
        print("""
        - - - My Analytics - - -
        
        1. [All Habits]
        2. [Daily - Weekly]
        """)

        # Check if the user has any habits to analyze
        if not ht.logged_in_user.habits:
            # If no habits exist, inform the user and prompt for return
            print("""\nYou don't have any habits yet!
            
            Navigate to 'My Habit Tracker' -> 'My Habits' to register a new habit!""")
            input("Press ENTER to return... ")
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
        print("(Type 'quit' at any time to exit the application)")
        print("\n        - - - [All Habits] Analytics - - -")
        habit_name, streak = analytics.longest_streak_all_habits()
        print(f"\n        >> Longest streak: {habit_name} with a {streak}-days streak")
        habit_name, count = analytics.most_completed_habit()
        print(f"        >> Most completed habit: {habit_name} with {count} completions")
        habit_name, count = analytics.least_completed_habit()
        print(f"        >> Least completed habit: {habit_name} with {count} completions")
        avg_streak = round(analytics.average_streak_all_habits(), 2)
        print(f"        >> Average streak length: {round(analytics.average_streak_length_habit(habit_name), 2)}")
        i = input(f"\nPress ENTER to go << Back to My Habit Tracker Menu...")

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
        print("(Type 'quit' at any time to exit the application)")
        print("\n        - - - [Daily - Weekly] Analytics - - -")

        print("\n        >> Longest streak <<")
        daily_name, daily_streak = analytics.longest_streak_by_periodicity("daily")
        print(f"        Daily: '{daily_name}' with a {daily_streak}-day streak")
        weekly_name, weekly_streak = analytics.longest_streak_by_periodicity("weekly")
        print(f"        Weekly: '{weekly_name}' with a {weekly_streak}-day streak")

        print("\n        >> Most completed habits <<")
        daily_name, daily_count = analytics.most_completed_by_periodicity("daily")
        print(f"        Daily: '{daily_name}' with {daily_count} completions")
        weekly_name, weekly_count = analytics.most_completed_by_periodicity("weekly")
        print(f"        Weekly: '{weekly_name}' with {weekly_count} completions")

        print("\n        >> Least completed habits <<")
        daily_name, daily_count = analytics.least_completed_by_periodicity("daily")
        print(f"        Daily: '{daily_name}' with {daily_count} completions <<")
        weekly_name, weekly_count = analytics.least_completed_by_periodicity("weekly")
        print(f"        Weekly: '{weekly_name}' with {weekly_count} completions <<")

        print("\n        >> Average streak length <<")
        avg_daily = round(analytics.average_streak_by_periodicity("daily"), 2)
        print(f"        Daily: {avg_daily} <<")
        avg_weekly = round(analytics.average_streak_by_periodicity("weekly"))
        print(f"        Weekly: {avg_weekly} <<")

        i = input(f"\nPress ENTER to go << Back to My Habit Tracker Menu...")

        # Check for exit command
        check_exit_cmd(i)

        return