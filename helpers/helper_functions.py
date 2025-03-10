import os
import sys
import time
import sqlite3
from typing import Any, Optional

from config import DB_FILEPATH

def confirm_input(attribute_name: str, value: str) -> Optional[str]:
    """
    Helper method to confirm input with the user.

    - asks the user to confirm their input (yes/no)
    - returns the value if "yes"
    - exits if "no"

    Parameters:
        attribute_name: The "type" of input being confirmed (e.g. "username", "habit_name").
        value: The value to confirm (e.g. the username or habit name the user chooses to assign).
    Returns:
        The confirmed value, or None if not confirmed.
    """
    while True:
        # Ask for confirmation
        print(f"You entered '{value}'. Is this correct? (yes/no): ")
        confirmation = input().lower().strip()

        if confirmation == "yes":
            print(f"You've successfully stored {value.title()} as your {attribute_name}!")
            return value
        elif confirmation == "no":
            print(f"Let's try again!")
            return None
        else:
            print("Invalid input! Please enter 'yes' or 'no'!")

def confirm_int_input(value: Any) -> Any | None:
    """
    Helper method to confirm numerical input with the user.
    Identical to confirm_input, only prints are different.
    """
    while True:
        print(f"You've chosen '{value}', is this correct? (yes/no): ")
        confirmation = input().lower().strip()
        if confirmation == "yes":
            print(f"You've chosen '{value}'!")
            return value
        elif confirmation == "no":
            print(f"Let's try again!")
            return None
        else:
            print("Invalid input! Please enter 'yes' or 'no'!")

def reload_menu_countdown() -> None:
    """
    Displays a countdown before returning.
    Allows visual feedback: the user has time to read the screen before it is reloaded (in most cases).
    """
    print("Reloading Menu in...")
    time.sleep(1)

    print("2")
    time.sleep(0.25)
    print(".")
    time.sleep(0.25)
    print(".")
    time.sleep(0.25)
    print(".")
    time.sleep(0.25)

    print("1")
    time.sleep(0.25)
    print(".")
    time.sleep(0.25)
    print(".")
    time.sleep(0.25)
    print(".")
    time.sleep(0.25)

def reload_cli():
    """
    Used to refresh the cli across various operations.
    Mostly used together with reload_menu_countdown.
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
                print("\Invalid input. Please try again!")
                reload_menu_countdown()