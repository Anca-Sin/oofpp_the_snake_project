from typing import List

from config import DB_FILEPATH

from core.habit import Habit
from helpers.helper_functions import db_connection

"""
add habit
load habits
save habits
delete habit
"""

def load_habits(selected_user) -> List[Habit]:
    """
    Loads all habits for the selected user.

    :return: A list of Habit objects.
    """
    connection = db_connection(DB_FILEPATH)
    cursor = connection.cursor()

    # Query for all habit names for the selected user
    cursor.execute("SELECT habit_name FROM habits WHERE user_id = ?", (selected_user.id,))
    habit_data = cursor.fetchall()

    habits = []
    for habit_row in habit_data:
        habit = Habit(name=habit_row[0])
        habits.append(habit)

    connection.close()
    return habits