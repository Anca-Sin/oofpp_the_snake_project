from datetime import datetime

from config import DB_FILEPATH

from manager_habit_db import save_habits
from core.user import User
from core.habit import Habit
from helpers.helper_functions import reload_menu_countdown, reload_cli, confirm_input


def complete_habit_today(selected_user: User, habit: Habit) -> None:
    """
    Marks a habit as completed for the current day.

    :param selected_user: The User object whose habit to complete.
    :param habit: The Habit object to complete.
    """
    # Use Habit's method to check_off_habit
    if habit.check_off_habit():
        save_habits(selected_user) # Save the updates to the db

def complete_habit_past(selected_user: User, habit: Habit) -> None:
    """Marks a habit as completed for a past date."""
    current_date = datetime.now().date()

    while True:
        reload_cli()
        date_str = input(f"Enter the date for completion (YYYY-MM-DD): ").strip()

        try:
            # Attempt to parse the date
            completion_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Validate it's not a future date
            if completion_date > current_date:
                print("Cannot complete habits for future dates!")
                reload_menu_countdown()
                return

            # Check if this date already has a completion
            # Let the user exit this "menu" if he wants
            elif completion_date in habit.completion_dates:
                print(f"""'{habit.name}' is already completed for {date_str}!
                
                You have the following options:
                1 - Register another completion
                2 - Return to the previous menu
                """)

                choice = input("\nEnter your choice (1-2): ").strip()

                if choice == "1":
                    return
                elif choice == "2":
                    habit_detail_menu
                else:
                    print("\nSorry, invalid input. Please try again!")
                    reload_menu_countdown()

            # If valid, confirm and break the loop
            else:
                confirmed = confirm_input("completion date", date_str)
                if confirmed:
                    habit.completion_dates.append(completion_date)
                    habit.streaks.get_current_streak(habit.frequency, habit.completion_dates)
                    save_habits(selected_user)
                    print(f"'{habit.name}' has been completed for {date_str}!")
                    reload_menu_countdown()
                    break

        except ValueError:
            print("Invalid date format! Please use YYYY-MM-DD format!")
            reload_menu_countdown()
            continue