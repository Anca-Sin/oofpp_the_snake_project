from datetime import datetime, date, timedelta
from typing import Optional

from helpers.colors import GRAY, RES, GREEN, RED
from .manager_habit_db import save_habits

from core.user import User
from core.habit import Habit
from helpers.helper_functions import reload_menu_countdown, confirm_input, check_exit_cmd


def _is_habit_completed(habit) -> bool:
    """
    Check if the habit is already completed.

    - for daily habits, checks if completed today
    - for weekly habits, checks if completed this week

    Returns:
        True if already completed, False otherwise.
    """
    today = datetime.now().date()

    if habit.frequency == "daily":
        # Check if habit was already completed today
        return today in habit.completion_dates

    elif habit.frequency == "weekly":
        # Calculate start of the current week (Monday)
        week_start = today - timedelta(days=today.weekday())
        # Check if habit was already completed this week
        return any(
            week_start <= completion_date <= week_start + timedelta(days=6)
            for completion_date in habit.completion_dates
        )

    return False  # If neither condition is met

def complete_habit_today(habit: Habit) -> Optional[date]:
    """
    Marks a habit as completed for today.

    - prevents duplicate completion

    Parameters:
        habit: The Habit object to complete.
    Returns:
        date: Today's date for db updates and streak calculations in the Database method it serves.
    """
    today = datetime.now().date()

    while True:
        print(f"\n{GRAY}Do you wish to complete{RES} '{habit.name}' {GRAY}for{RES} today?")
        choice = input(f"Type {GREEN}'yes'{RES} to confirm or {GRAY} ENTER << to exit{RES}: ").strip()

        # Check for exit command
        check_exit_cmd(choice)

        if choice == "yes":
            # Check if already completed for complete today.
            if _is_habit_completed(habit):
                print(f"\n'{habit.name}' has {RED}already{RES} been completed today!")
                input(f"{GRAY}ENTER << to return...{RES}")
                return None

            print(f"\n'{habit.name}' completed for {today} successfully!")
            input(f"{GRAY}ENTER << to return...{RES}")
            # Return today's date to the Database method
            return today
        elif choice == "":
            return None
        else:
            # Handle invalid input
            print("\nSorry, invalid input. Please try again!")
            input(f"{GRAY}ENTER << to continue...{RES}")

def complete_habit_past(habit: Habit) -> Optional[date]:
    """
    Marks a habit as completed for a past date.

    - prompts for a past date
    - validates date input (not future, proper format)
    - checks if the date already has a completion

    Parameters:
        habit: The Habit object to complete.
    Returns:
        date: The past completion date for db updates and streak calculations in the Database method it serves.
    """
    current_date = datetime.now().date()

    # Prompt for the date of the past completion or ENTER to exit
    while True:
        date_str = input(f"\n{GRAY}Enter the date to complete {RES}'{habit.name}'{GREEN} (YYYY-MM-DD){RES}{GRAY} or ENTER << to cancel{RES}: ").strip()

        # Check for exit command
        check_exit_cmd(date_str)

        # If the user presses ENTER without any date, exit
        if not date_str:
            return None # Return to Habit Detail Menu

        try:
            # Try to change the string input to date
            completion_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Validate it's not a future date
            if completion_date > current_date:
                print("\nCannot complete habits for future dates!")
                input(f"{GRAY}ENTER << to continue...{RES}")

            # Check if this date already has a completion
            # Let the user exit this "menu" if he wants
            elif completion_date in habit.completion_dates:
                print(f"\n'{habit.name}' is already completed for {date_str}!")
                input(f"{GRAY}ENTER << to return...{RES}")
                return None

            # Valid date that doesn't have a completion
            else:
                # Confirm the user's choice
                confirmed = confirm_input("completion date", date_str)
                if confirmed:
                    input(f"{GRAY}ENTER << to return...{RES}")
                    # Return date for the Database method
                    return completion_date
                else:
                    # If confirmed input is None on << ENTER
                    return None

        except ValueError:
            # Handle invalid date format
            print("\nInvalid date format! Please use YYYY-MM-DD format!")
            input(f"{GRAY}ENTER << to continue...{RES}")

def delete_completion(habit: Habit) -> Optional[date]:
    """
    Deletes a completion for a habit.

    - checks if there are any completions to delete
    - prompts for the date to delete
    - checks the date has a completion
    - confirms the deletions

    Parameters:
        habit: The Habit object containing the completion to delete.
    Returns:
        date: The deleted date for db updates and streak calculations in the Database method it serves.
    """
    # Check if there are no completions to delete
    if not habit.completion_dates:
        print(f"\nNo completions found for '{habit.name}'! {GRAY}ENTER << to return...{RES}")
        return None

    # Prompt for the date of the completion to delete or ENTER to exit
    while True:
        date_str = input(f"\n{GRAY}Enter the date to delete completion for {RES}'{habit.name}' {GREEN}(YYYY-MM-DD){RES}{GRAY} or ENTER << to cancel{RES}: ").strip()

        # If the user presses ENTER without any date, exit
        if not date_str:
            return None # Return to Habit Details Menu

        try:
            # Try to change the string input to date
            deletion_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Check if the entered date exists in the completion_dates
            if deletion_date in habit.completion_dates:
                # Confirm deletion
                while True:
                    choice = input(f"\n{GRAY}You entered {RES}'{deletion_date}'{GRAY}. Type 'yes' or {GRAY}ENTER << to cancel{RES}: ").strip()

                    # Check for exit command
                    check_exit_cmd(choice)

                    if choice == "yes":
                        print(f"You've successfully {RED}deleted{RES} {deletion_date} from {habit.name}'s completions!")
                        input(f"\n{GRAY}ENTER << to return...{RES}")
                        # Return date for the Database method
                        return deletion_date
                    else:
                        # Handle invalid input
                        print("\nSorry, invalid input. Please try again!")
                        input(f"{GRAY}ENTER << to continue...{RES}")

            # If chosen completion isn't in the completions list
            else:
                print(f"\nCompletion for {date_str} not found in {habit.name}'s completions list!")
                input(f"{GRAY}ENTER << to continue...{RES}")

        except ValueError:
            # Handle invalid date format
            print("\nInvalid date format! Please use YYYY-MM-DD format!")
            input(f"{GRAY}ENTER << to continue...{RES}")