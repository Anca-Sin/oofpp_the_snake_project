import os
import sys
import time
import sqlite3
from typing import Any

from config import DB_FILEPATH

from cli.main_menu import main_menu

def confirm_input(attribute_name: str, value: str) -> str | None:
    """Helper method to confirm input with the user."""
    while True:
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
    """Helper method to confirm numerical input with the user."""
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
    Allows the user time to read invalid input feedback.
    Displays a countdown message to simulate reloading.
    """
    print("Reloading Menu in...")
    time.sleep(1)
    print("""2
    ...
    """)
    time.sleep(1)
    print("""1
    ...
    """)
    time.sleep(1)

def db_connection(instance):
    """
    Attempts to connect to the db.
    If connection fails, prompts the user with retry options.

    :param instance: The HabitTracker instance.
    :return: Connection object or None
    """
    try:
        return sqlite3.connect(DB_FILEPATH)
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        time.sleep(1)
        print("Failed to connect to the database.")
        time.sleep(1)

        while True:
            reload_cli()
            print("""\nOptions:
            1. Retry database connection
            2. Return to main menu
            3. Exit the application
            """)

            choice = input("\nEnter your choice (1-3): ").strip()

            if choice == "1":
                print("Trying to re-establish your connection...")
                return db_connection(instance)
            elif choice == "2":
                print("Returning to main menu...")
                time.sleep(1)
                main_menu(instance)
                return
            elif choice == "3":
                print("Goodbye! Remember to stay on track!")
                time.sleep(1)
                sys.exit(0)
            else:
                print("\Invalid input. Please try again!")
                reload_menu_countdown()

def reload_cli():
    """Used to refresh the cli across various operations."""
    os.system('cls' if os.name == 'nt' else 'clear')