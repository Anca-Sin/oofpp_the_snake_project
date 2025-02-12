from datetime import datetime

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

            # Fail-safe for mistyping
            print(f"You entered '{self.username.title()}'. Is this correct? (yes/no):")
            confirmation = input().lower()

            if confirmation == "yes":
                print(f"You've successfully stored {self.username.title()} as your username!")
                break
            elif confirmation == "no":
                print("Let's try again!")