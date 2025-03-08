from datetime import datetime

from .manager_habit_db import save_habits

from core.user import User
from core.habit import Habit
from helpers.helper_functions import reload_menu_countdown, reload_cli, confirm_input

def complete_habit_today(selected_user: User, habit: Habit) -> None:
    """
    Marks a habit as completed for today.

    - uses Habit's method to check_off_habit
    - saves changes to the db
    Parameters:
        selected_user: The User object whose habit to complete.
        habit: The Habit object to complete.
    """
    if habit.check_off_habit():
        save_habits(selected_user)

def complete_habit_past(selected_user: User, habit: Habit) -> None:
    """
    Marks a habit as completed for a past date.

    - prompts for a past date
    - validates date input (not future, proper format)
    - checks if the date already has a completion
    - updates streaks if valid
    - saves changes to the db

    Parameters:
        selected_user: The User object whose habit to complete.
        habit: The Habit object to complete.
    """
    current_date = datetime.now().date()

    # Prompt for the date of the past completion or ENTER to exit
    while True:
        reload_cli()
        date_str = input(f"\nEnter the date to complete '{habit.name}' (YYYY-MM-DD) or ENTER to exit: ").strip()

        # If the user presses ENTER without any date, exit
        if not date_str:
            print("Exiting past completion menu.")
            reload_menu_countdown()
            return # Return to Habit Detail Menu

        try:
            # Attempt to parse the date string to a date object
            completion_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Validate it's not a future date
            if completion_date > current_date:
                print("Cannot complete habits for future dates!")
                reload_menu_countdown()
                continue

            # Check if this date already has a completion
            # Let the user exit this "menu" if he wants
            elif completion_date in habit.completion_dates:
                print(f"""'{habit.name}' is already completed for {date_str}!
                
                You have the following options:
                1 - Register another completion
                2 - Return to {habit.name}'s Details
                """)

                choice = input("\nEnter your choice (1-2): ").strip()

                if choice == "1":
                    continue # Restart loop
                elif choice == "2":
                    return
                else:
                    # Handle invalid input
                    print("\nSorry, invalid input. Please try again!")
                    reload_menu_countdown()
                    continue

            # Valid date that doesn't have a completion
            else:
                # Confirm the user's choice
                confirmed = confirm_input("completion date", date_str)
                if confirmed:
                    # Add the completion date
                    habit.completion_dates.append(completion_date)
                    # Update streak information
                    habit.streaks.get_current_streak(habit.frequency, habit.completion_dates)
                    # Save changes to the db
                    save_habits(selected_user)
                    print(f"'{habit.name}' has been completed for {date_str}!")
                    reload_menu_countdown()
                    return

        except ValueError:
            # Handle invalid date format
            print("Invalid date format! Please use YYYY-MM-DD format!")
            reload_menu_countdown()

def delete_completion(selected_user: User, habit: Habit) -> None:
    """
    Deletes a completion for a habit.

    - checks if there are any completions to delete
    - prompts for the date to delete
    - confirms the deletions
    - updates streaks after the deletion
    - saves changes to the db

    Parameters:
        selected_user: The User object whose habit completion to delete.
        habit: The Habit object containing the completion to delete.
    """
    # Check if there are no completions to delete
    if not habit.completion_dates:
        print(f"No completions found for '{habit.name}'")
        reload_menu_countdown()
        return

    # Prompt for the date of the completion to delete or ENTER to exit
    while True:
        reload_cli()
        date_str = input(f"\nEnter the date to delete for '{habit.name}' (YYYY-MM-DD) or ENTER to exit: ").strip()

        # If the user presses ENTER without any date, exit
        if not date_str:
            print("Exiting the deletion menu.")
            reload_menu_countdown()
            return # Return to Habit Details Menu

        try:
            # Parse the entered date
            completion_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Check if the entered date exists in the completion_dates
            if completion_date in habit.completion_dates:
                # Confirm deletion
                if confirm_input("completion date", date_str):
                    # Remove the completion
                    habit.completion_dates.remove(completion_date)
                    # Update streak information
                    habit.streaks.get_current_streak(habit.frequency, habit.completion_dates)
                    # Save changes to the db
                    save_habits(selected_user)

                    print(f"Completion on {date_str} has been deleted!")
                    reload_menu_countdown()
                    return

            else:
                # Handle invalid input
                print(f"Completion for {date_str} not found. Try again!")
                reload_menu_countdown()
                continue

        except ValueError:
            # Handle invalid date format
            print("Invalid date format! Please use YYYY-MM-DD format!")
            reload_menu_countdown()