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
            input("... Press ENTER to continue ...")

        elif choice == "2":
            # Display longest streak
            longest_streak = analytics.longest_streak_for_habit(habit.name)
            print(f"\n{habit.name}'s longest streak: {longest_streak}")
            input("... Press ENTER to continue ...")

        elif choice == "3":
            # Display average streak length
            average_streak = analytics.average_streak_length_habit(habit.name)
            print(f"\n{habit.name}'s average streak: {average_streak}")
            input("... Press ENTER to continue ...")

        elif choice == "4":
            # Return to Habit Details Menu
            return

        else:
            print("\nInvalid input! Please try again!")
            reload_menu_countdown()