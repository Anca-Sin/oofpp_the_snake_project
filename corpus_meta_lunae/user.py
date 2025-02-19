from datetime import datetime
from helper_functions import confirm_input

class User:
    """User creation class."""

    def __init__(self, username: str = "") - None:
        # Initialize user attributes with values passed during account creation
        self.username: str = username # Unique identifier for the user
        # Default to an empty string if no username is provided

    def user_name(self) -> None:
        """Prompts the user to type in a desired username."""
        while True:
            print("Please type in your desired username:")
            self.username = input().title()
            self.username = confirm_input("username", self.username)