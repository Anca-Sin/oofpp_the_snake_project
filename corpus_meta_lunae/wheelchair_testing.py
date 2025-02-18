from datetime import datetime
from habit import Habit

# Create a Habit instance to test
habit = Habit()
habit.name = "Test Habit"

# Set a custom frequency for the habit
habit.custom_frequency = (1, 2)  # 1-2 times per week
habit.frequency = "custom"

# Print initial state
print(f"Initial completions: {habit.completions}")

# Test checking off habit for the first time
print("\nTest 1: First check-off of the week.")
habit.check_off_habit()  # Should succeed
print(f"Completions after first check-off: {habit.completions}")

# Test checking off habit again within the same week (should be allowed up to 2 times)
print("\nTest 2: Second check-off of the week.")
habit.check_off_habit()  # Should still succeed as long as completions < max (2)
print(f"Completions after second check-off: {habit.completions}")

# Test exceeding the custom frequency (more than 5 completions)
print("\nTest 3: Attempting to exceed the custom frequency limit.")
habit.check_off_habit()  # Should not be allowed
print(f"Completions after exceeding custom frequency: {habit.completions}")
