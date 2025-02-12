from datetime import datetime

class User:
    """User creation class."""
    def __init__(self, username=None, gender=None):
        # Initialize user attributes with values passed during account creation
        self.username = username if username else ""  # Unique identifier for the user
        # Default to an empty string if no username/gender is provided
        self.gender = gender if gender else ""        # Gender for gender-specific logic


