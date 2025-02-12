from datetime import datetime
from helper_functions import confirm_input

class User:
    """User creation class."""
    def __init__(self, username=None, gender=None):
        # Initialize user attributes with values passed during account creation
        self.username = username if username else ""  # Unique identifier for the user
        # Default to an empty string if no username/gender is provided
        self.gender = gender if gender else ""        # Gender for gender-specific logic

    def user_name(self):
        """Prompts the user to type in a desired username."""
        while True:
            print("Please type in your desired username:")
            self.username = input().title()
            self.username = confirm_input("username", self.username)

    def user_gender(self):
        """Prompts the user to select either male/female gender."""
        while True:
            print("Please type in male/female to select a gender:")
            self.gender = input().title()
            self.gender = confirm_input("gender", self.gender)