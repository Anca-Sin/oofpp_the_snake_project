from corpus_meta_lunae.user import User

def test_user_class():
    # Test case 1: Create a user with a username and gender
    user1 = User(username="JohnDoe", gender="Male")
    print(f"Test 1 - User with username and gender: Username: {user1.username}, Gender: {user1.gender}")

    # Test case 2: Create a user without passing username and gender (uses default values)
    user2 = User()
    print(f"Test 2 - User with default values: Username: {user2.username}, Gender: {user2.gender}")

    # Test case 3: Create a user with only username, gender should default to ""
    user3 = User(username="JaneDoe")
    print(f"Test 3 - User with only username: Username: {user3.username}, Gender: {user3.gender}")

    # Test case 4: Create a user with only gender, username should default to ""
    user4 = User(gender="Female")
    print(f"Test 4 - User with only gender: Username: {user4.username}, Gender: {user4.gender}")


# Run the test
test_user_class()