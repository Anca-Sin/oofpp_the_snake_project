"""
This module contains utility functions used throughout the application for:
- user input confirmation with 2 use cases: strings and integers
- terminal ui management
- database connection
- app exit handling
"""

import os
import sys
import time
import sqlite3
from typing import Optional

from config import DB_FILEPATH
from helpers.text_formating import GRAY, RES, RED, BLUE, GREEN, ITAL, YELLOW


def invalid_input():
    """Standardizes the invalid input message."""
    input(f"\n{YELLOW}Invalid input!{RES} {enter()} to try again...")

def enter():
    """Standardizes the enter hint to return."""
    return f"{ITAL}{GRAY}ENTER <<{RES}"

def confirm_input(attribute_name: str, value: str) -> Optional[str]:
    """
    Confirms input with the user.

    Parameters:
        attribute_name: The "type" of input being confirmed (e.g. "username", "habit_name").
        value: The value to confirm.
    Returns:
        The confirmed value if confirmed, None otherwise.
    """
    while True:
        # Ask for confirmation
        confirmation = input(
            f"\nType '{GREEN}yes{RES}' to confirm '{GREEN}{value}{RES}' or {enter()} to exit: "
        ).lower().strip()

        if confirmation == "yes":
            return value
        elif confirmation == "":
            return None
        else:
            invalid_input()

def reload_cli():
    """
    Refreshes the cli across various operations.
    Simplifies implementation throughout the project.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def db_connection(instance) -> Optional[sqlite3.Connection]:
    """
    Attempts to connect to the db.
    If connection fails, provides retry options.

    Parameters:
        instance: The HabitTracker instance or DB_FILEPATH.
    Returns:
        Connection object to the db, or exits if unable to connect.
    """
    # Try to connect to the db
    try:
        return sqlite3.connect(DB_FILEPATH)

    # Handle connection error
    except sqlite3.Error as e:
        # Provides options to retry, return to main menu, or exit
        while True:
            reload_cli()
            print(f"""\nDatabase connection error: {e}
            Failed to connect to the database.
            
            Options:
            1. Retry database connection
            2. Return to main menu
            3. Exit the application
            """)

            choice = input("\nEnter your choice (1-3): ").strip()

            if choice == "1":
                print("Trying to re-establish your connection...")
                return db_connection(instance)
            elif choice == "2":
                # Return to main menu
                from cli.main_menu import main_menu
                print("Returning to main menu...")
                time.sleep(1)
                main_menu(instance)
            elif choice == "3":
                # Exit the application
                print("Goodbye! Remember to stay on track!")
                time.sleep(1)
                sys.exit(0)
            else:
                invalid_input()

def check_exit_cmd(command: str) -> bool:
    """
    Checks if the input is an exit command.

    Args:
        command: User input to check
    Returns:
        True if the command is an exit command, False otherwise
    """
    if command.lower().strip() == "quit":
        print(f"\nGoodbye! {GREEN}(^_^)/{RES}")
        time.sleep(0.40)
        print("           .")
        time.sleep(0.40)
        print("           .")
        time.sleep(0.40)
        print("           .")
        time.sleep(0.40)
        print(f"""
{BLUE}-------------------------{RES}
{RED}REMEMBER TO STAY ON TRACK{RES}
{BLUE}-------------------------{RES}
        """)
        time.sleep(0.40)
        print("           .")
        time.sleep(0.40)
        print("           .")
        time.sleep(0.40)
        print("           .")
        time.sleep(0.40)
        reload_cli()
        sys.exit(0)
    return False

def exit_msg(logged_in_user=None):
    """Displays exit message and selected user if any."""
    print(f"{GRAY}(Type '{RES}quit{GRAY}' at any time to exit the application){RES}")
    if logged_in_user:
        print(f"{GRAY}Logged in as:{RES} {GREEN}{logged_in_user.username}{RES}")

def cancel_operation(operation_name: str = "Operation"):
    """
    Displays a standard message for canceled operations.

    Parameters:
        operation_name: A string representing the name of the operation canceled.
                        Defaults to "Operation".
    """
    print(f"\n{GRAY}{operation_name} {RED}canceled!{RES}")
    time.sleep(1)
    print(f"\n{GRAY}No changes will be saved...")
    time.sleep(1)
    print(f"\nReturning...{RES}")
    time.sleep(1)

def setup_header(setup):
    """
    Displays setup header for new user and new habit.

    Args:
        setup: A string describing the setup - either "User" or "Habit"
    """
    print()
    print()
    print(f"""
    {GREEN}        - - - New {setup} Setup - - -{RES}

                """)

def save_entry_msg(entry):
    """
    Displays confirmation after successful operation with a small countdown.

    Args:
        entry: A string describing what was saved - names, completions past
    """
    print(f"\n{GRAY}Saving... {GREEN}(^_^)/{RES}")
    time.sleep(1)
    print(f"\n'{entry}' {GREEN}saved!{RES}")
    time.sleep(1)
    print(f"\n{GRAY}Returning...{RES}")
    time.sleep(1)

def good_job(msg: str = "right"):
    """Friendly motivational message after completions."""
    print(f"\n{GRAY}You're {msg} on track! {GREEN}(^_^)/{RES} {GRAY}Keep it up!{RES}")

def wavey_mctrackface():
    """Friendly funny message to greet the user."""
    input(f"""
        Hey there! 
            
        {GRAY}I'm Wavey McTrackface {GREEN}(^_^)/{RES} {GRAY}- your personal habit-tracking sidekick!{RES}
            
        Press {enter()} to get started!
        """)