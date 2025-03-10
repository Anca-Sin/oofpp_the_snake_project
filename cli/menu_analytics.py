"""
Menu: Analytics - For viewing statistics on one habit or across all habits

menu_analytics_one_habit: Submenu of Habit Details Menu
menu_analytics_all_habits: Submenu of My Habit Tracker Menu
"""
from core.habit import Habit
from helpers.helper_functions import reload_cli, reload_menu_countdown


def menu_analytics_one_habit(ht, habit: Habit) -> None:
    """
    Displays the Analytics Menu for a selected habit.

    Parameters:
        ht: The HabitTracker instance that manages the application state.
        habit: The selected Habit object to analyze.
    """
    # Get the Analytics instance from the HabitTracker
    analytics = ht.analytics

    while True:
        # Clear the screen and display the menu header
        reload_cli()
        print(f"""- - - {habit.name}'s Analytics - - -

        1. Current streak
        2. Longest streak
        3. Average streak length
        4. Return to Habit Details Menu
        """)

        # Get user input
        choice = input("\nEnter your choice (1-4): ").strip()

        # Handle menu options
        if choice == "1":
            # Display current streak
            current_streak = habit.streaks.current_streak
            print(f"\n{habit.name}'s current streak: {current_streak}")
            input("Press ENTER to continue...")

        elif choice == "2":
            # Display longest streak
            longest_streak = analytics.longest_streak_for_habit(habit.name)
            print(f"\n{habit.name}'s longest streak: {longest_streak}")
            input("Press ENTER to continue...")

        elif choice == "3":
            # Display average streak length
            average_streak = analytics.average_streak_length_habit(habit.name)
            print(f"\n{habit.name}'s average streak: {average_streak}")
            input("Press ENTER to continue...")

        elif choice == "4":
            # Return to Habit Details Menu
            return

        else:
            # Handle invalid input
            print("\nInvalid input! Please try again!")
            reload_menu_countdown()

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
        print("""- - - My Analytics - - -
        
        1. [All Habits] Longest streak
        2. [All Habits] Most completed habit
        3. [All Habits] Least completed habit
        4. [All Habits] Average streak length
        5. [Daily - Weekly] Longest streaks
        6. [Daily - Weekly] Most completed habits
        7. [Daily - Weekly] Least completed habits
        8. [Daily - Weekly] Average streak length
        9. Return to My Habit Tracker Menu
        """)

        # Check if the user has any habits to analyze
        if not ht.logged_in_user.habits:
            # If no habits exist, inform the user and prompt for return
            print("""\nYou don't have any habits yet!
            
            Navigate to 'My Habit Tracker' -> 'My Habits' to register a new habit!""")
            input("\nPress ENTER to return... ")
            # Return to My Habit Tracker Menu
            return

        # If user has registered habits continue to prompt for choice
        else:
            # Get user choice
            choice = input("\nEnter your choice (1-9): ").strip()

            # Handle menu options
            if choice == "1":
                # [All Habits] Longest streak
                habit_name, streak = analytics.longest_streak_all_habits()
                print(f"\nYour longest streak is {streak} for '{habit_name}'!")
                input("\nPress ENTER to continue... ")

            elif choice == "2":
                # [All Habits] Most completed habit
                habit_name, count = analytics.most_completed_habit()
                print(f"\nYour most completed habit is '{habit_name}' with {count} completions!")
                input("\nPress ENTER to continue... ")

            elif choice == "3":
                # [All Habits] Least completed habit
                habit_name, count = analytics.least_completed_habit()
                print(f"\nYour least completed habit is '{habit_name}' with {count} completions!")
                input("\nPress ENTER to continue... ")

            elif choice == "4":
                # [All Habits] Average streak length
                avg_streak = analytics.average_streak_all_habits()
                print(f"\nYour average streak length across all habits is {avg_streak}!")
                input("\nPress ENTER to continue... ")

            elif choice == "5":
                # [Daily] Longest streak
                daily_name, daily_streak = analytics.longest_streak_by_periodicity("daily")
                print(f"\nDaily: Your longest streak is '{daily_streak}' for '{daily_name}'!")

                # [Weekly] Longest streak
                weekly_name, weekly_streak = analytics.longest_streak_by_periodicity("weekly")
                print(f"\nWeekly: Your longest streak is '{weekly_streak}' for '{weekly_name}'!")
                input("\nPress ENTER to continue... ")

            elif choice == "6":
                # [Daily] Most completed habit
                daily_name, daily_count = analytics.most_completed_by_periodicity("daily")
                print(f"\nDaily: Your most completed habit is '{daily_name}' with {daily_count} completions!")

                # [Weekly] Most completed weekly
                weekly_name, weekly_count = analytics.most_completed_by_periodicity("weekly")
                print(f"\nWeekly: Your most completed habit is '{weekly_name}' with {weekly_count} completions!")
                input("\nPress ENTER to continue... ")

            elif choice == "7":
                # [Daily] Least completed habit
                daily_name, daily_count = analytics.least_completed_by_periodicity("daily")
                print(f"\nDaily: Your least completed habit is '{daily_name}' with {daily_count} completions!")

                # [Weekly] Least completed habit
                weekly_name, weekly_count = analytics.least_completed_by_periodicity("weekly")
                print(f"\nWeekly: Your least completed habit is '{weekly_name}' with {weekly_count} completions!")
                input("\nPress ENTER to continue... ")

            elif choice == "8":
                # [Daily] Average streak length
                avg_daily = analytics.average_streak_by_periodicity("daily")
                print(f"\nDaily: Your average streak length is {avg_daily}!")

                # [Weekly] Average streak length
                avg_weekly = analytics.average_streak_by_periodicity("weekly")
                print(f"\nWeekly: Your average streak length is {avg_weekly}!")
                input("\nPress ENTER to continue... ")

            elif choice == "9":
                # Return to My Habit Tracker Menu
                return

            else:
                # Handle invalid input
                print("\nInvalid input! Please try again!")
                reload_menu_countdown()