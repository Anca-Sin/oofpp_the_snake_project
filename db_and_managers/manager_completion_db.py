from datetime import datetime

from helpers.colors import GRAY, RES, GREEN, RED
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
    print(f"\n{GRAY}Do you wish to complete{RES} '{habit.name}' {GRAY}for{RES} today?")
    choice = input(f"Type {GREEN}'yes'{RES} to confirm or {GRAY} ENTER << to exit{RES}: ").strip()

    # Check for exit command
    check_exit_cmd(choice)

    if choice == "yes":
        habit.check_off_habit()
        save_habits(selected_user)
        input(f"{GRAY}ENTER << to continue...{RES}")
    elif choice == "":
        return
    else:
        # Handle invalid input
        print("\nSorry, invalid input. Please try again!")
        input(f"{GRAY}ENTER << to continue...{RES}")

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
        date_str = input(f"\n{GRAY}Enter the date to complete {RES}'{habit.name}'{GREEN} (YYYY-MM-DD){RES}{GRAY} or ENTER << to cancel{RES}: ").strip()

        # Check for exit command
        check_exit_cmd(date_str)

        # If the user presses ENTER without any date, exit
        if not date_str:
            return # Return to Habit Detail Menu

        try:
            # Attempt to parse the date string to a date object
            completion_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Validate it's not a future date
            if completion_date > current_date:
                print("\nCannot complete habits for future dates!")
                input(f"{GRAY}ENTER << to continue...{RES}")

            # Check if this date already has a completion
            # Let the user exit this "menu" if he wants
            elif completion_date in habit.completion_dates:
                print(f"\n'{habit.name}' is already completed for {date_str}!")
                input(f"{GRAY}ENTER << to continue...{RES}")

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
                    input(f"{GRAY}ENTER << to continue...{RES}")
                    return
                else:
                    # If confirmed input is None on << ENTER
                    return

        except ValueError:
            # Handle invalid date format
            print("\nInvalid date format! Please use YYYY-MM-DD format!")
            input(f"{GRAY}ENTER << to continue...{RES}")

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
        print(f"\nNo completions found for '{habit.name}'! {GRAY}ENTER << to continue...{RES}")
        return

    # Prompt for the date of the completion to delete or ENTER to exit
    while True:
        date_str = input(f"\n{GRAY}Enter the date to delete completion for {RES}'{habit.name}' {GREEN}(YYYY-MM-DD){RES}{GRAY} or ENTER << to cancel{RES}: ").strip()

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
                    choice = input(f"\n{GRAY}You entered {RES}'{deletion_date}'{GRAY}. Type 'yes' or {GRAY}ENTER << to cancel{RES}: ").strip()

                    # Check for exit command
                    check_exit_cmd(choice)

                    if choice == "yes":
                        print(f"You've successfully {RED}deleted{RES} {deletion_date} from {habit.name}'s completions!")
                        # Remove the completion
                        habit.completion_dates.remove(deletion_date)
                        # Update streak information
                        habit.streaks.get_current_streak(habit.frequency, habit.completion_dates, deletion_date)
                        # Save changes to the db
                        save_habits(selected_user)
                        input(f"\n{GRAY}ENTER << to continue...{RES}")
                        return # Exit after deletion
                    elif choice == "":
                        print(f"\nLet's try again!")
                        return
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