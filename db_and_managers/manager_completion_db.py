from datetime import datetime

from .manager_habit_db import save_habits

from core.user import User
from core.habit import Habit
from helpers.helper_functions import reload_menu_countdown, confirm_input, check_exit_cmd


def complete_habit_today(selected_user: User, habit: Habit) -> None:
    """
    Marks a habit as completed for today.

    - uses Habit's method to check_off_habit
    - saves changes to the db
    Parameters:
        selected_user: The User object whose habit to complete.
        habit: The Habit object to complete.
    """
    choice = input(f"\nDo you wish to complete '{habit.name}' for today? (yes/no): ").strip()

    # Check for exit command
    check_exit_cmd(choice)

    if choice == "yes":
        habit.check_off_habit()
        save_habits(selected_user)
        input("\nPress ENTER to continue... ")
    elif choice == "no":
        reload_menu_countdown()
        return
    else:
        # Handle invalid input
        print("\nSorry, invalid input. Please try again!")
        input("\nPress ENTER to continue... ")

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
        date_str = input(f"\nEnter the date to complete '{habit.name}' (YYYY-MM-DD) or ENTER to exit: ").strip()

        # Check for exit command
        check_exit_cmd(date_str)

        # If the user presses ENTER without any date, exit
        if not date_str:
            print("Exiting past completion menu.")
            return # Return to Habit Detail Menu

        try:
            # Attempt to parse the date string to a date object
            completion_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Validate it's not a future date
            if completion_date > current_date:
                print("Cannot complete habits for future dates!")
                input("\nPress ENTER to continue... ")

            # Check if this date already has a completion
            # Let the user exit this "menu" if he wants
            elif completion_date in habit.completion_dates:
                print(f"'{habit.name}' is already completed for {date_str}!")
                input("\nPress ENTER to continue... ")

            # Valid date that doesn't have a completion
            else:
                # Confirm the user's choice
                confirmed = confirm_input("completion date", date_str)
                if confirmed:
                    # Add the completion date
                    habit.completion_dates.append(completion_date)
                    # Update streak information
                    habit.streaks.get_current_streak(habit.frequency, habit.completion_dates, completion_date)
                    # Save changes to the db
                    save_habits(selected_user)
                    print(f"'{habit.name}' has been completed for {date_str}!")
                    input("\nPress ENTER to continue... ")
                    return

        except ValueError:
            # Handle invalid date format
            print("Invalid date format! Please use YYYY-MM-DD format!")
            input("\nPress ENTER to continue... ")

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
        input("\nPress ENTER to continue... ")
        return

    # Prompt for the date of the completion to delete or ENTER to exit
    while True:
        date_str = input(f"\nEnter the date to delete for '{habit.name}' (YYYY-MM-DD) or ENTER to exit: ").strip()

        # If the user presses ENTER without any date, exit
        if not date_str:
            return # Return to Habit Details Menu

        try:
            # Parse the entered date
            deletion_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Check if the entered date exists in the completion_dates
            if deletion_date in habit.completion_dates:
                # Confirm deletion
                while True:
                    choice = input(f"\nYou entered '{deletion_date}'. Is this correct? (yes/no): ").strip()

                    # Check for exit command
                    check_exit_cmd(choice)

                    if choice == "yes":
                        print(f"You've successfully deleted {deletion_date} from {habit.name}'s completions!")
                        # Remove the completion
                        habit.completion_dates.remove(deletion_date)
                        # Update streak information
                        habit.streaks.get_current_streak(habit.frequency, habit.completion_dates, deletion_date)
                        # Save changes to the db
                        save_habits(selected_user)
                        input("\nPress ENTER to continue... ")
                        return # Exit after deletion
                    elif choice == "no":
                        print(f"Let's try again!")
                        input("\nPress ENTER to continue... ")
                        break # Go back to asking for a date
                    else:
                        # Handle invalid input
                        print("\nSorry, invalid input. Please try again!")
                        input("\nPress ENTER to continue... ")
                        continue

            # If chosen completion isn't in the completions list
            else:
                print(f"Completion for {date_str} not found in {habit.name}'s completions list!")
                input("\nPress ENTER to continue... ")

        except ValueError:
            # Handle invalid date format
            print("Invalid date format! Please use YYYY-MM-DD format!")
            input("\nPress ENTER to continue... ")