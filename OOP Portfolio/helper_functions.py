from typing import Any
import time

def confirm_input(attribute_name: str, value: str) -> str | None:
    """Helper method to confirm input with the user."""
    while True:
        print(f"You entered '{value}'. Is this correct? (yes/no):")
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