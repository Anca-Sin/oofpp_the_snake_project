import time
from typing import List

from helpers.helper_functions import confirm_input

class User:
    """
    Represents a user in the habit tracking system.

    The User class serves as the central entity that owns habits and interacts with the db.
    Each user has a unique username and user_id.

    Attributes:
        username (str): The username of the user.
        user_id (int): The id from the db of the user.
        habits (List[Habit]): A list of habits associated with the user.
    """

    def __init__(self, username: str = "", user_id: int = None) -> None:
        """Initializes a User object with a username and an empty list of habits."""
        from .habit import Habit      # Avoid circular imports
        self.username: str = username
        self.user_id: int = user_id
        self.habits: List[Habit] = [] # Starts with an empty list of habits

    def create_username(self) -> None:
        """
        Creates a new username.

        - handles input and confirmation
        - checks if the username already exists in the db
        """
        # Avoid circular imports
        from db_and_managers.manager_user_db import username_exists, select_user

        while True:
            # Ask user for username
            print("Please type in your desired username (Press ENTER to exit): ")
            username = input().title().strip()

            # Exit the loop if "ENTER"
            if not username:
                print("Exiting user creation...")
                select_user()

            # Check if the username already exists
            elif username_exists(username):
                print(f"Username '{username}' is taken! Please try again!")
                time.sleep(1)

            else:
                # Confirm the choice
                confirmed_username = confirm_input("username", username)

                # If the choice is confirmed
                if confirmed_username is not None:
                    self.username = confirmed_username
                    time.sleep(1)
                    return