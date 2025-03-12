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
    Displays the Analytics Menu across all habits.

    - 1-4. statistics across all habits
    - 5-8. statistics broken down by periodicity ("daily" or "weekly)

    Parameters:
        ht: The HabitTracker instance that manages the application state.
    """
    # Get the Analytics instance from the HabitTracker
    analytics = ht.analytics

    while True:
        # Clear the screen and display the menu header
        reload_cli()
        print("(Type 'quit' at any time to exit the application)")
        print("""
        - - - My Analytics - - -
        
        1. [All Habits] Longest streak
        2. [All Habits] Most completed habit
        3. [All Habits] Least completed habit
        4. [All Habits] Average streak length
        5. [Daily - Weekly] Longest streaks
        6. [Daily - Weekly] Most completed habits
        7. [Daily - Weekly] Least completed habits
        8. [Daily - Weekly] Average streak length
        9. << Back to My Habit Tracker Menu
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
            choice = input("\nEnter your choice (1-9): ").strip()

            # Check for exit command
            check_exit_cmd(choice)

            # Handle menu options
            if choice == "1":
                # [All Habits] Longest streak
                print("\n1. [All Habits] Longest streak:")
                habit_name, streak = analytics.longest_streak_all_habits()
                print(f"\n>> '{habit_name}' with a {streak}-streak <<")
                input("Press ENTER to continue... ")

            elif choice == "2":
                # [All Habits] Most completed habit
                print("\n2. [All Habits] Most completed habit:")
                habit_name, count = analytics.most_completed_habit()
                print(f"\n>> '{habit_name}' with {count} completions <<")
                input("Press ENTER to continue... ")

            elif choice == "3":
                # [All Habits] Least completed habit
                print("\n3. [All Habits] Least completed habit:")
                habit_name, count = analytics.least_completed_habit()
                print(f"\n>> '{habit_name}' with {count} completions <<")
                input("Press ENTER to continue... ")

            elif choice == "4":
                # [All Habits] Average streak length
                print("\n4. [All Habits] Average streak length:")
                avg_streak = round(analytics.average_streak_all_habits(), 2)
                print(f"\n>> {avg_streak} <<")
                input("Press ENTER to continue... ")

            elif choice == "5":
                # [Daily] Longest streak
                print("\n5. [Daily - Weekly] Longest streaks")
                daily_name, daily_streak = analytics.longest_streak_by_periodicity("daily")
                print(f"\n>> Daily: '{daily_name}' with a {daily_streak}-streak <<")
                input("Press ENTER to continue... ")

                # [Weekly] Longest streak
                weekly_name, weekly_streak = analytics.longest_streak_by_periodicity("weekly")
                print(f"\n>> Weekly: '{weekly_name}' with a {weekly_streak}-streak <<")
                input("Press ENTER to continue... ")

            elif choice == "6":
                # [Daily] Most completed habit
                print("\n6. [Daily - Weekly] Most completed habits")
                daily_name, daily_count = analytics.most_completed_by_periodicity("daily")
                print(f"\n>> Daily: '{daily_name}' with {daily_count} completions <<")
                input("Press ENTER to continue... ")

                # [Weekly] Most completed weekly
                weekly_name, weekly_count = analytics.most_completed_by_periodicity("weekly")
                print(f"\n>> Weekly: '{weekly_name}' with {weekly_count} completions <<")
                input("Press ENTER to continue... ")

            elif choice == "7":
                print("\n7. [Daily - Weekly] Least completed habits")
                # [Daily] Least completed habit
                daily_name, daily_count = analytics.least_completed_by_periodicity("daily")
                print(f"\n>> Daily: '{daily_name}' with {daily_count} completions <<")
                input("Press ENTER to continue... ")

                # [Weekly] Least completed habit
                weekly_name, weekly_count = analytics.least_completed_by_periodicity("weekly")
                print(f"\n>> Weekly: '{weekly_name}' with {weekly_count} completions <<")
                input("Press ENTER to continue... ")

            elif choice == "8":
                # [Daily] Average streak length
                print("\n8. [Daily - Weekly] Average streak length")
                avg_daily = round(analytics.average_streak_by_periodicity("daily"), 2)
                print(f"\n>> Daily: {avg_daily} <<")
                input("Press ENTER to continue... ")

                # [Weekly] Average streak length
                avg_weekly = round(analytics.average_streak_by_periodicity("weekly"))
                print(f"\n>> Weekly: {avg_weekly} <<")
                input("Press ENTER to continue... ")

            elif choice == "9":
                # Return to My Habit Tracker Menu
                return

            else:
                # Handle invalid input
                print("\nInvalid input! Please try again!")
                reload_menu_countdown()