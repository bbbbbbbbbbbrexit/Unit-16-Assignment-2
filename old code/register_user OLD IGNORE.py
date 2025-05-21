from clear_console import clr
import re

def registerUser(userID):
    while True:
        clr()
        firstName = input("Enter your first name: ").strip().lower()
        if not re.match(r"^[a-zA-Z\s\-]+$", firstName):
            input("First name can only contain letters, spaces, or hyphens. Press enter to try again.\n")
            continue
        break

    while True:
        clr()
        lastName = input("Enter your last name: ").strip().lower()
        if not re.match(r"^[a-zA-Z\s\-]+$", lastName):
            input("Last name can only contain letters, spaces, or hyphens. Press enter to try again.\n")
            continue
        break

    while True:
        clr()
        emailAddress = input("Enter your email address: ").strip().lower()
        if not re.fullmatch(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", emailAddress):
            input("Invalid email format. Press enter to try again.\n")
            continue
        break

    while True:
        clr()
        userPassword = input("Enter a password for your account: ")
        if (len(userPassword) < 8 or
            not re.search(r"[A-Z]", userPassword) or
            not re.search(r"[a-z]", userPassword) or
            not re.search(r"\d", userPassword) or
            not re.search(r"[!@#$%^&*(),.?\":{}|<>]", userPassword)):
            input("Password must include the following:\n"
                  "At least 8 characters\nAt least one uppercase letter\nAt least one lowercase letter\nAt least one digit\nAt least one special character\nPress enter to try again.")
            continue
        clr()
        if input("Confirm the password entered: ") == userPassword:
            break
        else:
            print("Does not match entered password. Press enter to try again.\n")

    userData = (userID, firstName, lastName, emailAddress, userPassword, False)
    return userData