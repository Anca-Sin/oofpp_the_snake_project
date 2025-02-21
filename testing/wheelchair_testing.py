import unittest
from corpus_meta_lunae.user_database import UserDatabase

class TestUserDatabase(unittest.TestCase):
    def test_load_users(self):
        # Create an instance of UserDatabase
        db = UserDatabase("test_users.json")

        # Write a simple test data directly into the file
        test_data = '[{"username": "Alice", "habits": []}, {"username": "Bob", "habits": []}]'
        db.filepath.write_text(test_data)  # Write this test data to the JSON file

        # Load users using the load_users method
        users = db.load_users()

        # Simple assertions
        self.assertEqual(len(users), 2)  # Ensure we have 2 users
        self.assertEqual(users[0].username, "Alice")  # Check if first user's username is Alice
        self.assertEqual(users[1].username, "Bob")  # Check if second user's username is Bob

if __name__ == "__main__":
    unittest.main()
