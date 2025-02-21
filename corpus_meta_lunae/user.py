# from datetime import datetime
from .helper_functions import confirm_input
from .habit import Habit
from typing import List

class User:
    """
    Represents a user in the habit tracking system.

    Attributes:
        username (str): The username the user registers to use.
        habits (List[Habit]): A list of habits associated with the user.
    """

    def __init__(self, username: str = "") -> None:
        """
        Initializes a User object with a username and an empty list of habits.

        :arg username (str): The username which defaults to an empty string if not provided.
        """
        self.username: str = username # Unique identifier for the user
        self.habits: List[Habit] = [] # List to store the user's habits

    def user_name(self) -> None:
        """Prompts the user to type in a desired username."""
        while True:
            print("Please type in your desired username:")
            self.username = input().title()
            self.username = confirm_input("username", self.username)