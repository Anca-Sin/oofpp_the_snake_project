"""
Menu: Analytics - For viewing statistics on one habit or across all habits
"""

from core.habit import Habit
from helpers.helper_functions import reload_cli, reload_menu_countdown


def menu_analytics_one_habit(ht, habit: Habit) -> None:
    """
    Displays the Analytics Menu from Habit's Detail Menu

    :param ht: The HabitTracker instance.
    :param habit: The Habit object to analyze.
    """
    analytics = ht.analytics

    while True:
        reload_cli()
        print(f"""- - - {habit.name}'s Analytics - - -

        1. Current streak
        2. Longest streak
        3. Average streak length
        4. Return to Habit Details Menu
        """)

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            # Display current streak
            current_streak = habit.streaks.current_streak
            print(f"\n{habit.name}'s current streak: {current_streak}")
            input("Press ENTER to continue ...")

        elif choice == "2":
            # Display longest streak
            longest_streak = analytics.longest_streak_for_habit(habit.name)
            print(f"\n{habit.name}'s longest streak: {longest_streak}")
            input("Press ENTER to continue ...")

        elif choice == "3":
            # Display average streak length
            average_streak = analytics.average_streak_length_habit(habit.name)
            print(f"\n{habit.name}'s average streak: {average_streak}")
            input("Press ENTER to continue ...")

        elif choice == "4":
            # Return to Habit Details Menu
            return

        else:
            print("\nInvalid input! Please try again!")
            reload_menu_countdown()

def menu_analytics_all_habits(ht) -> None:
    """
    Displays the Analytics Menu across all habits.

    :param ht: The HabitTracker instance.
    """
    analytics = ht.analytics

    while True:
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

        # Prompt if user has no habits to analyze and prompt return
        if not ht.logged_in_user.habits:
            print("\nYou don't have any habits yet!")
            input("\nPress ENTER to return... ")

        # If user has registered habits continue to prompt for choice
        else:
            choice = input("\nEnter your choice (1-4): ").strip()

            if choice == "1":
                # Longest streak across all habits
                habit_name, streak = analytics.longest_streak_all_habits()
                print(f"\nYour longest streak is {streak} for '{habit_name}'!")
                input("\nPress ENTER to return... ")

            elif choice == "2":
                # Most completed habit across all habits
                habit_name, count = analytics.most_completed_habit()
                print(f"\nYour most completed habit is '{habit_name}' with {count} completions!")
                input("\nPress ENTER to return... ")

            elif choice == "3":
                # Least completed habit across all habits
                habit_name, count = analytics.least_completed_habit()
                print(f"\nYour least completed habit is '{habit_name}' with {count} completions!")
                input("\nPress ENTER to return... ")

            elif choice == "4":
                # Average streak length across all habits
                avg_streak = analytics.average_streak_all_habits()
                print(f"\nYour average streak length across all habits is {avg_streak}!")
                input("\nPress ENTER to return... ")

            elif choice == "5":
                # Longest streaks for daily habits
                daily_name, daily_streak = analytics.longest_streak_by_periodicity("daily")
                print(f"\nDaily: Your longest streak is '{daily_streak}' for '{daily_name}'!")

                # Longest streaks for weekly habits
                weekly_name, weekly_streak = analytics.longest_streak_by_periodicity("weekly")
                print(f"\nWeekly: Your longest streak is '{weekly_streak}' for '{weekly_name}'!")
                input("\nPress ENTER to return... ")

            elif choice == "6":
                # Most completed daily habit
                daily_name, daily_count = analytics.most_completed_by_periodicity("daily")
                print(f"\nDaily: Your most completed habit is '{daily_name}' with {daily_count} completions!")

                # Most completed weekly habit
                weekly_name, weekly_count = analytics.most_completed_by_periodicity("weekly")
                print(f"\nWeekly: Your most completed habit is '{weekly_name}' with {weekly_count} completions!")
                input("\nPress ENTER to return... ")

            elif choice == "7":
                # Least completed daily habit
                daily_name, daily_count = analytics.least_completed_by_periodicity("daily")
                print(f"\nDaily: Your least completed habit is '{daily_name}' with {daily_count} completions!")

                # Least completed weekly habit
                weekly_name, weekly_count = analytics.least_completed_by_periodicity("weekly")
                print(f"\nWeekly: Your least completed habit is '{weekly_name}' with {weekly_count} completions!")
                input("\nPress ENTER to return... ")

            elif choice == "8":
                # Average streak length for daily habits
                avg_daily = analytics.average_streak_by_periodicity("daily")
                print(f"\nDaily: Your average streak length is {avg_daily}!")

                # Average streak length for weekly habits
                avg_weekly = analytics.average_streak_by_periodicity("weekly")
                print(f"\nWeekly: Your average streak length is {avg_weekly}!")
                input("\nPress ENTER to return... ")

            elif choice == "9":
                # Return to My Habit Tracker Menu
                return

            else:
                print("\nInvalid input! Please try again!")
                reload_menu_countdown()