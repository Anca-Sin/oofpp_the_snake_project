"""
Habit completion management database module.

Provides behind the scenes database operations for completions related functionality, including:
- checking if a habit has already been completed
- marking habits as complete for today or past dates inputted by the user
- completion deletion
- managing validation and user interaction
"""

from datetime import datetime, date, timedelta
from typing import Optional

from helpers.text_formating import RES, GREEN, RED
from core.habit import Habit
from helpers.helper_functions import confirm_input, check_exit_cmd, good_job, enter, invalid_input


def _is_habit_completed(habit) -> bool:
    """
    Check if the habit is already completed for it's given periodicity.

    - for daily habits, checks if completed today
    - for weekly habits, checks if completed this week

    Args:
        habit: The Habit object to check completion for.
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

    return False

def complete_habit_today(habit: Habit) -> Optional[date]:
    """
    Marks a habit as completed for today.

    - prevents duplicate completion for the same period

    Args:
        habit: The Habit object to complete.
    Returns:
        date: Today's date for db updates and streak calculations (in the Database method it serves).
        None: If completion is canceled or habit is already completed.
    """
    today = datetime.now().date()

    while True:
        choice = input(
            f"\nType '{GREEN}yes{RES}' to complete for today or {enter()} to exit: "
        ).strip()

        # Check for exit command
        check_exit_cmd(choice)

        if choice == "yes":
            # Check if already completed for complete today.
            if _is_habit_completed(habit):
                input(f"\n'{habit.name}' is {RED}already{RES} completed today! {enter()} to return...")
                return None

            good_job() # Helper
            input(f"\n'{habit.name}' {GREEN}completed{RES}! {enter()} to return...")
            # Return today's date to the Database method
            return today
        elif choice == "":
            return None
        else:
            # Handle invalid input
            invalid_input()

def complete_habit_past(habit: Habit) -> Optional[date]:
    """
    Marks a habit as completed for a past date.

    - prompts for a past date
    - validates date input (not future, proper format)
    - checks if the date already has a completion

    Args:
        habit: The Habit object to complete.
    Returns:
        date: The past completion date for db updates and streak calculations in the Database method it serves.
        None: If completion canceled.
    """
    current_date = datetime.now().date()

    # Prompt for the date of the past completion or ENTER to exit
    while True:
        date_str = input(
            f"\nEnter the date as {GREEN}(YYYY-MM-DD){RES} or {enter()} to exit: "
        ).strip()

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
                input(f"\nYou can't sneak in future dates! {RED}(v_v)*{RES} {enter()} to return...")

            # Check if this date already has a completion
            # Let the user exit this "menu" if he wants
            elif completion_date in habit.completion_dates:
                input(f"\n'{habit.name}' is {RED}already{RES} completed for {date_str}! {enter()} to return...")
                return None

            # Valid date that doesn't have a completion
            else:
                # Confirm the user's choice
                confirmed = confirm_input("completion date", date_str)
                if confirmed:
                    good_job() # Helper
                    input(f"{enter()} to return...")
                    # Return date for the Database method
                    return completion_date
                else:
                    # If user cancels the confirmation
                    return None

        except ValueError:
            # Handle invalid date format
            input(f"\nInvalid date! {enter()} to continue...")

def delete_completion(habit: Habit) -> Optional[date]:
    """
    Deletes a completion record for a habit.

    - checks if there are any completions to delete
    - prompts for the date to delete
    - checks the date has a completion
    - confirms the deletions

    Args:
        habit: The Habit object to delete the completion for.
    Returns:
        date: The deleted date for db updates and streak recalculations in the Database method it serves.
        None: If deletion canceled.
    """
    # Check if there are no completions to delete
    if not habit.completion_dates:
        input(f"\n{RED}No{RES} completions found for '{habit.name}'! {enter()} to return...")
        return None

    # Prompt for the date of the completion to delete or ENTER to exit
    while True:
        date_str = input(
            f"\nEnter the date as {GREEN}(YYYY-MM-DD){RES} or {enter()} to exit: "
        ).strip()

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
                    choice = input(
                        f"\nType '{GREEN}yes{RES}' to {RED}delete{RES} {deletion_date} or {enter()} to exit: "
                    ).strip()

                    # Check for exit command
                    check_exit_cmd(choice)

                    if choice == "yes":
                        input(
                            f"{RED}Deleted{RES} {deletion_date} from your track! {enter()} to return..."
                        )
                        # Return date for the Database method
                        return deletion_date
                    else:
                        # Handle invalid input
                        input(f"{invalid_input()} {enter()} to continue...")

            # If chosen completion isn't in the completions list
            else:
                input(f"\n'{habit.name}' has no completion on {date_str}! {enter()} to return...")
                return None

        except ValueError:
            # Handle invalid date format
            input(f"\nInvalid date! {enter()} to continue...")