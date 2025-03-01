# from datetime import datetime
from .helper_functions import confirm_input
from .habit import Habit
from typing import List

from .user_database import UserDatabase


class User:
    """
    Represents a user in the habit tracking system.

    Attributes:
        username (str): The username the user registers to use.
        habits (List[Habit]): A list of habits associated with the user.
    """

    def __init__(self, username: str = "", db: UserDatabase = None) -> None:
        """
        Initializes a User object with a username and an empty list of habits.

        :param username: The username which defaults to an empty string if not provided.
        :param db: An instance of Database to interact with the db
        """
        self.username: str = username # Unique identifier for the user
        self.habits: List[Habit] = [] # List to store the user's habits
        self.db = db

    def create_username(self) -> None:
        """Prompts the user to type in a desired username."""
        while True:
            print("Please type in your desired username:")
            username = input().title()
            # Confirm the choice
            confirmed_username = confirm_input("username", username)

            if confirmed_username is not None: # If user confirmed with "yes"
                self.username = confirmed_username
                return