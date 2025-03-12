"""
Calendar view for habit completions.

- provides calendar visualization for habit completions in the terminal
- displays a monthly calendar with completion days marked
- allows users to track habit completions patterns visually
- can add a past date completion
- can delete a completion
"""
import calendar
from datetime import datetime

from core.habit import Habit
from db_and_managers.database import Database
from helpers.helper_functions import reload_cli, check_exit_cmd, reload_menu_countdown, exit_msg
from helpers.colors import BLUE, RES, RED, GRAY

# Create a db instance
db = Database()

def display_habit_calendar(
        habit: Habit,
        year=datetime.now().date().year,
        month=datetime.now().date().month
) -> None:
    """
    Displays a monthly calendar view of a habit's completions.

    - outputs a text based calendar to the terminal with weekdays as columns
    - days marked when habit was completed

    Parameters:
        habit: The Habit object whose completions to display.
        year: Year to display (defaults to current year).
        month: Month to display (defaults to current month).
    """
    # Get the calendar for the month
    # monthcalendar -> List[weeks], Week[days]
    # Days outside the month = 0
    cal = calendar.monthcalendar(year, month)

    # Create a list of days that have completions for this month
    completion_days = []
    for date in habit.completion_dates:
        if date.year == year and date.month == month:
            completion_days.append(date.day)

    # Get full month name
    month_name = calendar.month_name[month]

    print(f"\n{BLUE}- - - '{habit.name}' Calendar View - - -{RES}")
    print(f"\n{month_name} {year}")
    print(f"{GRAY}---------------------------------{RES}")
    print("Mon  Tue  Wed  Thu  Fri  Sat  Sun")

    # Print calendar with completions marked down
    for week in cal:
        week_str = ""
        for day in week:
            if day == 0:
                # Day "outside" the month
                week_str += "     " # 5 spaces
            elif day in completion_days:
                # Completion day: Mark day with [ ]
                if day < 10:
                    # Extra space for single digits
                    week_str += f"{RED}[{RES} {day}{RED}]{RES}"
                else:
                    week_str += f"{RED}[{RES}{day}{RED}]{RES}"
            else:
                # Non-completion day
                if day < 10:
                    # Extra space for single digits
                    week_str += "  " + str(day) + " "
                else:
                    week_str += " " + str(day) + " "
        print(week_str)
    print(f"{GRAY}---------------------------------{RES}")

def view_completions_calendar(ht, habit: Habit) -> None:
    """
    Calendar view for habit completions.

    Allows:
    - navigating between months (backward, forward, jump to a specific month)
    - registering a past completion
    - deleting a completion

    Parameters:
        ht: The HabitTracker instance that manages the application state.
        habit: The Habit object whose completions to display and interact with.
    """
    # Set initial year and month to current date
    year = datetime.now().date().year
    month = datetime.now().date().month

    while True:
        # Clear screen and print header
        reload_cli()
        exit_msg(ht.logged_in_user)

        # Display calendar for current month
        display_habit_calendar(habit, year, month)

        # Navigation options
        print(f"""
        {BLUE}- - - Calendar Navigation Options - - -{RES}
        
        P - Previous month
        N - Next month
        G - Go to specific month
        """)

        # Completion options
        print(f"""
        {BLUE}- - - Completion Options - - -{RES}
        
        1 - Complete for today
        2 - Complete for a past date
        3 - Delete a completion
        """)
        print(f"""
        {GRAY}ENTER << Back to Habit Details Menu - - -{RES}
        """)

        choice = input("\nEnter your choice: ").strip().lower()

        # Check for exit command
        check_exit_cmd(choice)

        if choice == "p":
            # Navigate to previous month
            month -= 1
            # Handle January to December
            if month < 1:
                month = 12
                year -= 1

        elif choice == "n":
            # Navigate to next month
            month += 1
            # Handle December to January
            if month > 12:
                month = 1
                year += 1

        elif choice == "g":
            try:
                # Go to specific month
                month_input = input("\nEnter month (1-12): ").strip()
                year_input = input("Enter year (YYYY): ").strip()

                # Check for exit commands
                check_exit_cmd(month_input)
                check_exit_cmd(year_input)

                # Convert inputs to ints
                new_month = int(month_input)
                new_year = int(year_input)

                # Validate choices
                if 1 <= new_month <= 12 and 2023 <= new_year <= 2100:
                    month = new_month
                    year = new_year
                else:
                    # Handle invalid integer input
                    print("\nInvalid month or year. Please try again!")
                    input("Press ENTER to continue...")
            except ValueError:
                # Handle invalid string input
                print("\nInvalid input (only numbers). Please try again!")
                input("Press ENTER to continue...")

        elif choice == "1":
            # Complete for today
            db.complete_habit_today(ht.logged_in_user, habit)

        elif choice == "2":
            # Complete for a past date
            db.complete_habit_past(ht.logged_in_user, habit)

        elif choice == "3":
            # Delete a completion
            db.delete_completion(ht.logged_in_user, habit)

        elif choice == "":
            # Return to My Habit Details Menu
            return

        else:
            # Handle invalid input
            print("\nInvalid input! Please try again!")
            reload_menu_countdown()