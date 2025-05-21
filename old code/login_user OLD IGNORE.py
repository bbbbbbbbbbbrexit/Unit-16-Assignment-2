from register_user import registerUser
from clear_console import clr
from universal_menu import universalMenu
import numpy as np

def newUser():
    # Makes the new user ID
    # all it does is get last ID in the file and adds 1
    newID = str(int(user_data[(len(user_data) - 1), 0]) + 1)

    # if the new ID is less than 4 digits it adds 0's to the front
    # so that it is always 4 digits
    while len(newID) < 4:
        newID = "0" + newID

    # Calls the registerUser function
    newUser = registerUser(newID)

    # Adds the new user to the user_data array
    user_data = np.append(user_data, [newUser], axis=0)
    # and saves it to the file
    np.savetxt(filePath, user_data, fmt="%s", delimiter=",")

    input("Created new account. Press enter to try again.")
    return

def userLogin():
    while True:
        userEmail = input("Enter your email address: ")
        userPassword = input("Enter your password: ")

        for i in range(len(user_data)):
            if userEmail == user_data[i, 3] and userPassword == user_data[i, 4]:
                input("Login successful. Enter to continue.")
                userLine = i
                return True, userLine  # <-- Return both values

        clr()
        print("Invalid email address or password.\n")
        choice = universalMenu(["Try again", "Return to start menu"])
        if choice == "1":
            continue
        elif choice == "2":
            return False, None  # <-- Return two values, userLine is None if not found

def loginMenu():
    while True:
        # Brings in the user data from the file
        # and makes it global so it can be used in other functions
        global filePath
        global user_data
        filePath = "user_data.csv"
        user_data = np.loadtxt(filePath, delimiter=",", dtype=str)

        # Makes the user choose if they want to register or login
        # and calls the right function
        clr()
        print("Welcome to the Car Rental System")
        choice = universalMenu(["Register", "Login"])

        if choice == "1":
            newUser()
        elif choice == "2":
            clr()
            result, userLine = userLogin()
            if result == True:
                return userLine
        else:
            input("Invalid choice. Press enter to try again.")
