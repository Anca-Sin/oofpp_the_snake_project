from habit import Habit
from helper_functions import confirm_input

habit = Habit()

# Test 1: Single value input (e.g., "3")
print("\nTest 1: Single value input (e.g., '3')")
habit.set_custom_frequency()
print(f"Custom Frequency: {habit.custom_frequency}, Frequency: {habit.frequency}")

# Test 2: Range input (e.g., "3-5")
print("\nTest 2: Range input (e.g., '3-5')")
habit.set_custom_frequency()
print(f"Custom Frequency: {habit.custom_frequency}, Frequency: {habit.frequency}")