# noinspection PyShadowingNames

from .analytics import Analytics
from .helper_functions import reload_menu_countdown
from .user_database import UserDatabase
from .habit import Habit
import os
import time

class HabitTracker:
    """
    Main class to manage users, habit creation and tracking, streaks, and analytics.
    """

    def __init__(self):
        """
        Initializes the habit tracker.
        - Connects to the UserDatabase (handles storage and retrieval)
        - Optionally handles multiple users, but no login required (just for my exercise)
        """
        self.db = UserDatabase()   # Interacts with the local SQLite DB
        self.logged_in_user = None # Hypothetical "logged_in"

    def start(self) -> None:
        """
        Starts the Habit Tracker app.
        - Greets the user and allows username selection, or allows creating a new user
        - After the selection, the main menu is displayed
        """
        print("-- 'Corpus Meta Lunae' -- Habit Tracker --")

        # Select or create a user
        self.logged_in_user = self.select_user() # Store the returned user
        # Load their data
        self.load_user_data()
        # Show the main menu
        self.main_menu()

    def select_user(self):
        """
        Prompts the user to select or create/delete a username.

        :return: The selected User object.
        """
        return self.db.select_user()

    def load_user_data(self):
        """Loads the habits for the current user from the db."""
        # Need new method in UserDatabase

    def main_menu(self):
        """Displays the main menu and handles user navigation."""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("""- - - Main Menu - - -
            
            1. My Habit Tracker
            2. Select a different user
            3. Delete this user
            4. Exit
            """)

            choice = input("\nEnter your choice (1-4): ").strip()

            if choice == "1":
                self.my_habit_tracker()
            elif choice == "2":
                self.logged_in_user = self.select_user()
                self.load_user_data()
            elif choice == "3":
                self.db.delete_user()
            elif choice == "4":
                print("\nUntil next time! Do your best to stay on track!")
            else:
                print("\nSorry, invalid input. Please try again!")
                reload_menu_countdown()

    def my_habit_tracker(self):
        """Displays the habit tracker menu and handles user navigation."""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("""- - - My Habit Tracker - - -
            
            1. My Habits
            2. My Analytics
            3. Back to Main Menu
            """)

            choice = input("\nEnter your choice (1-3): ").strip()

            if choice == "1":
                self.habits_menu()
            elif choice == "2":
                self.analytics_menu()
            elif choice == "3":
                break # Return to the main_menu's loop
            else:
                print("\nSorry, invalid input. Please try again!")
                reload_menu_countdown()

    def habits_menu(self):
        """Displays the habits menu and handles user navigation."""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("""- - - My Habits - - -
            
            1. Register new habit
            2. List all habits
            3. Daily habits
            4. Weekly habits
            5. Back to main menu
            """)

            choice = input("\nEnter your choice (1-5): ").strip()

            if choice == "1":
                self.register_new_habit()
            elif choice == "2":
                self.list_habits()
            elif choice == "3":
                self.list_daily_habits()
            elif choice == "4":
                self.list_weekly_habits()
            elif choice == "5":
                break # Return to the main_menu's loop
            else:
                print("\nSorry, invalid option. Please try again!")
                reload_menu_countdown()

    def analytics_menu(self):
        """Displays the analytics menu and handles user navigation."""
        # Create Analytics object for the current user
        analytics = Analytics(self.logged_in_user)

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("""- - - My Analytics - - -
            
            1. Longest streak across all habits
            2. Most completed habit
            3. Least completed habit
            4. Back to main menu
            """)

            choice = input("\nEnter your choice (1-4): ").strip()

            if choice == "1":
                analytics.longest_streak_all_habits()
            elif choice == "2":
                analytics.most_completed_habit()
            elif choice == "3":
                analytics.least_completed_habit()
            elif choice == "4":
                break
            else:
                print("\nSorry, invalid option. Please try again!")
                reload_menu_countdown()

    def register_new_habit(self, frequency_preset=None):
        """Guides the user through a new habit creation."""
        os.system('cls' if os.name == 'nt' else 'clear')
        new_habit = Habit()
        new_habit.habit_name()

        if frequency_preset:
            # Use the frequency preset
            new_habit.frequency = frequency_preset
            print(f"\nFrequency automatically set to {frequency_preset}.")
        else:
            # Let the user chose the frequency
            new_habit.habit_frequency()

        new_habit.creation_date()

        # Add the habit to the user's list
        self.logged_in_user.habits.append(new_habit)

        # Save to db
        self.db.save_habits(self.logged_in_user)
        print(f"\n{new_habit.name} creation process completed!")
        reload_menu_countdown()

    def list_habits(self):
        """
        Lists only daily habits and allows the user to select one for detailed view.
        Uses the analytics module's functional programming methods.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        # Get all habits (using Analytics)
        analytics = Analytics(self.logged_in_user)
        all_habits = analytics.list_all_habits()

        # Check if there are no registered habits
        if not all_habits:
            print("""You don't have any habits yet.
            Please register a new habit!
            """)
            reload_menu_countdown()
            return # Return to the habits menu

        # Display all habits with numbering
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("""- - - My Habits - - -
            
            """)
            for idx, habit in enumerate(self.logged_in_user.habits, 1): # Start indexing at 1, instead of default 0
                print(f"{idx}. {habit.name} ({habit.frequency})")

            # Add extra option to go back to previous menu at the end
            # Calculate back option indexing according to number of habits
            habits_number = len(all_habits)
            back_option_idx = habits_number + 1
            print(f"{back_option_idx}. Back to my habits menu")

            # Get user selection
            choice = input(f"\nEnter your choice (1-{back_option_idx}): ")

            if 1 <= int(choice) <= habits_number:
                # Show detailed manu for selected habit
                self.habit_detail_menu(all_habits[int(choice) - 1]) # Adjust back to 0 indexing
                # Exit the loop after selecting a habit or returning from the detail menu
                break
            elif int(choice) == back_option_idx:
                break # Return to My Habits menu
            else:
                print("\nSorry, invalid input. Please try again!") # Handle invalid input and re-run the loop
                reload_menu_countdown()

    def list_daily_habits(self):
        """
        Lists only daily habits and allows the user to select one for detailed view.
        Uses the analytics module's functional programming methods.
        If no daily habit exists, offers to create one.
        """
        # Get daily habits (using Analytics)
        analytics = Analytics(self.logged_in_user)
        daily_habits = analytics.list_habits_by_periodicity("daily")

        # Check if there are no daily habits
        if not daily_habits:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("You don't have any daily habits yet!")
                time.sleep(1)
                # Ask the user if they want to create a daily habit or return to the previous menu
                print("""\nPlease chose between option 1 or 2:
                
                1. Create a new daily habit
                2. Back to my habits menu                
                """)

                choice = input(f"\nEnter your choice (1-2): ")

                if choice == "1":
                    self.register_new_habit(frequency_preset="daily")
                    return
                elif choice == "2":
                    return  # Return to My Habits menu
                else:
                    print("\nSorry, invalid input. Please try again!")
                    reload_menu_countdown()

        # Display daily habits with numbering
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("""- - - Daily Habits - - -
            
            """)
            for idx, habit in enumerate(daily_habits, 1): # Start indexing at 1
                print(f"{idx}. {habit.name}")

            # Add extra option to go back to previous menu at the end
            # Calculate back option indexing according to number of habits
            habits_number = len(daily_habits)
            back_option_idx = habits_number + 1
            print(f"{back_option_idx}. Back to my habits menu")

            # Get user selection
            choice = input(f"\nEnter your choice (1-{back_option_idx}): ")

            if 1 <= int(choice) <= habits_number:
                # Show detailed manu for selected habit
                self.habit_detail_menu(daily_habits[int(choice) - 1]) # Adjust back to 0 indexing
                # Exit the loop after selecting a habit or returning from the detail menu
                break
            elif int(choice) == back_option_idx:
                break # Return to My Habits menu
            else:
                print("\nSorry, invalid input. Please try again!")
                reload_menu_countdown()

    def list_weekly_habits(self):
        """
        Lists only weekly habits and allows the user to select one for detailed view.
        Uses the analytics module's functional programming methods.
        If no weekly habit exists, offers to create one.
        """
        # Get weekly habits (using Analytics)
        analytics = Analytics(self.logged_in_user)
        weekly_habits = analytics.list_habits_by_periodicity("weekly")

        # Check if there are no daily habits
        if not weekly_habits:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("You don't have any weekly habits yet!")
                time.sleep(1)
                # Ask the user if they want to create a weekly habit or return to the previous menu
                choice = input("""\nPlease chose between 1 or 2:
                
                1. Create a new weekly habit
                2. Back to my habits menu
                
                """).strip()

                if choice == "1":
                    self.register_new_habit(frequency_preset="weekly")
                    return
                elif choice == "2":
                    return  # Return to My Habits menu
                else:
                    print("Sorry, invalid input. Please try again!")
                    reload_menu_countdown()

        # Display weekly habits with numbering
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("""- - - Weekly Habits - - -
            
            """)
            for idx, habit in enumerate(weekly_habits, 1):  # Start indexing at 1
                print(f"{idx}. {habit.name}")

            # Add extra option to go back to previous menu at the end
            # Calculate back option indexing according to number of habits
            habits_number = len(weekly_habits)
            back_option_idx = habits_number + 1
            print(f"{back_option_idx}. Back to my habits menu")

            # Get user selection
            choice = input(f"\nEnter your choice (1-{back_option_idx}): ")

            if 1 <= int(choice) <= habits_number:
                # Show detailed manu for selected habit
                self.habit_detail_menu(weekly_habits[int(choice) - 1])  # Adjust back to 0 indexing
                # Exit the loop after selecting a habit or returning from the detail menu
                break
            elif int(choice) == back_option_idx:
                break  # Return to My Habits menu
            else:
                print("\nSorry, invalid input. Please try again!")  # Handle general invalid input and re-run the loop
                reload_menu_countdown()

    def habit_detail_menu(self, habit: Habit) -> None:
        """Shows detail menu for a selected habit and allows for completion/analysis."""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"""- - - {habit.name}'s Details - - -
            
            1. Completion
            2. Delete completion
            3. {habit.name}'s Analytics
            4. Back            
            """)

            choice = input("\nEnter your choice (1-4): ").strip()

            if choice == "1":
                self.completion_menu(habit)
            elif choice == "2":
                self.habit_analytics_menu(habit)
            elif choice == "3":
                break
            else:
                print("\nSorry, invalid input. Please try again!")
                reload_menu_countdown()

    def completion_menu(self, habit: Habit) -> None:
        """
        Shows completion menu for a selected habit and allows for:
        - completion of habit
        - completion deletion
        - deletion of habit
        """
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"""- - - {habit.name}'s Details - - -

                    1. Complete habit today
                    2. Complete habit past date
                    3. Delete a completion
                    4. Delete habit
                    5. Back
                    """)

            choice = input("\nEnter your choice (1-5): ").strip()

            if choice == "1":
                self.db.complete_habit_today(habit)
            elif choice == "2":
                self.db.complete_habit_past(habit)
            elif choice == "3":
                self.db.delete_completion(habit)
            elif choice == "4":
                self.db.delete_habit(habit)
                break # Exit after deleting habit
            elif choice == "5":
                break
            else:
                print("\nSorry, invalid input. Please try again!")
                reload_menu_countdown()

    def habit_analytics_menu(self, habit):
        if choice == "1":
            get_current_streak()
            get_longest_streak_habit()
            average_streak_lenght()
            all_time_completions_count()
            creation_date()