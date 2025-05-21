# Importing the necessary libraries
from clear_console import clr
from universal_menu import universalMenu
import numpy as np
import re

def userLogin():
    global user_data
    while True:
        attempts = 0
        # Makes user choose between loging in or registering
        clr()
        choice = universalMenu(["Login", "Register"])

        # If the user chooses to login
        clr()
        if choice == "1":
            while attempts < 3:
                # Asks for the email address and password
                userEmail = input("Enter your email address: ").lower()
                userPassword = input("Enter your password: ")
                clr()

                # Checks each account in user_data to see if the email and password match
                for i in range(len(user_data)):
                    # If the email and password match it returns with userData
                    if userEmail == user_data[i, 3] and userPassword == user_data[i, 4]:
                        clr()
                        input("Login successful. Enter to continue.")
                        userData = user_data[i]
                        return userData

                # If the email and password dont match any of the accounts
                # It adds 1 to the attempts
                attempts += 1
                # If the attempts are 3 it breaks out of the loop
                if attempts == 3:
                    clr()
                    input("Too many attempts in a session.")
                # If the attempts are less than 3 it makes the user try again
                else:
                    print("Invalid email address or password. Try again.\n")
        # If the user chooses to register
        elif choice == "2":
            # It first askes for the first name
            while True:
                clr()
                firstName = input("Enter your first name: ").strip().lower()
                # It checks if the first name is valid
                # It can only contain letters, spaces, or hyphens
                if not re.match(r"^[a-zA-Z\s\-]+$", firstName):
                    input("First name can only contain letters, spaces, or hyphens. Press enter to try again.\n")
                    continue
                break
            # Then asks for the last name
            while True:
                clr()
                lastName = input("Enter your last name: ").strip().lower()
                # Again, it checks if the input is valid
                if not re.match(r"^[a-zA-Z\s\-]+$", lastName):
                    input("Last name can only contain letters, spaces, or hyphens. Press enter to try again.\n")
                    continue
                break
            # Then asks for the email address
            while True:
                clr()
                emailAddress = input("Enter your email address: ").strip().lower()
                # It checks if the email address is actually an email address
                # And it also checks if the email address valid and if its already in use
                if not re.fullmatch(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", emailAddress):
                    input("Invalid email format. Press enter to try again.\n")
                    continue
                for i in range(len(user_data)):
                    # If the email and password match it returns with userData
                    if emailAddress == user_data[i, 3]:
                        input("Email address already in use. Press enter to try again.\n")
                break
            # Then asks for the password
            while True:
                clr()
                userPassword = input("Enter a password for your account: ")
                # It checks if the password is strong enough
                # It has to be at least 8 characters long, have capital and lowercase letters, have a number and have a special character.
                if (len(userPassword) < 8 or
                    not re.search(r"[A-Z]", userPassword) or
                    not re.search(r"[a-z]", userPassword) or
                    not re.search(r"\d", userPassword) or
                    not re.search(r"[!@#$%^&*(),.?\":{}|<>]", userPassword)):
                    input("Password must include the following:\n"
                        "At least 8 characters\nAt least one uppercase letter\nAt least one lowercase letter\nAt least one digit\nAt least one special character\nPress enter to try again.")
                    continue
                clr()
                # Then it asks the user to confirm the password
                if input("Confirm the password entered: ") == userPassword:
                    break
                else:
                    print("Does not match entered password. Press enter to try again.\n")

            # Gets last ID in the file and adds 1
            newID = str(int(user_data[(len(user_data) - 1), 0]) + 1)

            # if the new ID is less than 4 digits it adds 0's to the front
            # so that it is always 4 digits
            while len(newID) < 4:
                newID = "0" + newID

            # Makes a new user with the new ID and the other information
            # and sets the admin status to False
            newUser = (newID, firstName, lastName, emailAddress, userPassword, False)

            # Adds the new user to the user_data array
            user_data = np.append(user_data, [newUser], axis=0)
            # and saves it to the file
            np.savetxt(filePath, user_data, fmt="%s", delimiter=",")

            input("Created new account. Press enter to continue.")












# Program start
while True:
    global filePath
    global user_data
    global userData
    filePath = "Car Rental Service/car_data.csv"
    user_data = np.loadtxt(filePath, delimiter=",", dtype=str, skiprows=1)
    userData = userLogin()

    if userData[5] == "True":
        while True:
            clr()
            choice = universalMenu(["Manage Cars for Rent", "Manage Accounts", "Manage your Account", "Exit"])
            if choice == "1":
                print("Manage Cars for Rent")
            elif choice == "2":
                print("Manage Accounts")
            elif choice == "3":
                print("Manage your account")
            elif choice == "4":
                print("Exiting.")
                break
    else:
        while True:
            clr()
            # Calls the loginMenu function
            choice = universalMenu(["Browse Cars for Rent", "Manage Bookings", "Manage your Account", "Exit"])
            if choice == "1":
                print("Browse Cars for Rent")
            elif choice == "2":
                print("Manage Bookings")
            elif choice == "3":
                print("Manage your Account")
            elif choice == "4":
                print("Exiting.")
                break


