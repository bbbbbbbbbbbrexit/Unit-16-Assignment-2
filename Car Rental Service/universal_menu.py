def universalMenu(menuOptions):
    # Displays the menu options
    for idx, option in enumerate(menuOptions, start=1):
        print(f"{option} [{idx}]")
    choice = input("Please select an option: ")

    # Validates the choice
    if choice.isdigit() and 1 <= int(choice) <= len(menuOptions):
            return choice
    else:
        print("Invalid option. Try again.\n")
    return choice