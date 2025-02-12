def confirm_input(attribute_name, value):
    """Helper method to confirm input with the user."""
    while True:
        print(f"You entered '{value}'. Is this correct? (yes/no):")
        confirmation = input().lower()
        if confirmation == "yes":
            print(f"You've successfully stored {value.title()} as your {attribute_name}!")
            return value
        elif confirmation == "no":
            print(f"Let's try again!")
