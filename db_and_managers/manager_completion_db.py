
from config import DB_FILEPATH

from manager_habit_db import save_habits
from core.user import User
from core.habit import Habit
from helpers.helper_functions import reload_menu_countdown


def complete_habit_today(selected_user: User, habit: Habit) -> None:
    """
    Marks a habit as completed for the current day.

    :param selected_user: The User object whose habit to complete.
    :param habit: The Habit object to complete.
    """
    # Use Habit's method to check_off_habit
    if habit.check_off_habit():
        save_habits(selected_user) # Save the updates to the db

    reload_menu_countdown()