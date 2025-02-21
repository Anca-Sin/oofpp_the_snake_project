import unittest
from corpus_meta_lunae.user_database import UserDatabase
from corpus_meta_lunae.user import User
from corpus_meta_lunae.habit import Habit

class TestUserDatabase(unittest.TestCase):
    def test_save_users(self):
        # Create a UserDatabase instance
        db = UserDatabase("test_users.json")

        # Create sample users
        user1 = User("Alice")
        habit1 = Habit()
        habit1.name = "Exercise"
        habit1.frequency = "daily"
        user1.habits.append(habit1)

        user2 = User("Bob")
        habit2 = Habit()
        habit2.name = "Read"
        habit2.frequency = "weekly"
        user2.habits.append(habit2)

        users = [user1, user2]

        # Save the users to the JSON file
        db.save_users(users)

        # Load the users back from the file
        loaded_users = db.load_users()

        # Check if the number of users is correct
        self.assertEqual(len(loaded_users), 2)

        # Check if user data is saved correctly
        self.assertEqual(loaded_users[0].username, "Alice")
        self.assertEqual(len(loaded_users[0].habits), 1)
        self.assertEqual(loaded_users[0].habits[0].name, "Exercise")

        self.assertEqual(loaded_users[1].username, "Bob")
        self.assertEqual(len(loaded_users[1].habits), 1)
        self.assertEqual(loaded_users[1].habits[0].name, "Read")

    def tearDown(self):
        """Remove the test file after the test"""
        db = UserDatabase("test_users.json")
        db.filepath.unlink()  # Remove the test file to clean up

if __name__ == "__main__":
    unittest.main()
