from habit import Habit

habit = Habit()
habit.name = "Stretching"
habit.frequency = "weekly"

success = habit.check_off_habit()
assert success == True

success = habit.check_off_habit()
assert success == False