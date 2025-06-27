# Full Version of Cleaned Car Rental Application with Dashboard, Admin, and Booking

import sys
import numpy as np
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QLineEdit, QMessageBox, QStackedLayout, QHBoxLayout, QListWidget, QInputDialog,
)
from PyQt5.QtCore import Qt


# Data Loading
# -------------------------------

filePath = "Car Rental Service/user_data.csv"
try:
    user_data = np.loadtxt(filePath, delimiter=",", dtype=str)
except Exception as e:
    print(f"Error loading user data: {e}")
    user_data = np.empty((0, 6), dtype=str)

filePath = "Car Rental Service/car_data.csv"
try:
    car_data = np.loadtxt(filePath, delimiter=",", dtype=str)
except Exception as e:
    print(f"Error loading car data: {e}")
    car_data = np.empty((0, 11), dtype=str)

filePath = "Car Rental Service/payment_data.csv"
try:
    payment_data = np.loadtxt(filePath, delimiter=",", dtype=str)
except Exception as e:
    print(f"Payment data not found. Starting fresh. ({e})")
    payment_data = np.empty((0, 6), dtype=str)

userData = None  


# Helper Functions
# -------------------------------

def saveUserData():
    filePath = "Car Rental Service/user_data.csv"
    np.savetxt(filePath, user_data, fmt="%s", delimiter=",")

def saveCarData():
    filePath = "Car Rental Service/car_data.csv"
    np.savetxt(filePath, car_data, fmt="%s", delimiter=",")
    
def savePaymentData():
    filePath = "Car Rental Service/payment_data.csv"
    np.savetxt(filePath, payment_data, fmt="%s", delimiter=",")

def showMessage(title, text):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.exec_()

def clearLoginFields():
    emailInput.clear()
    passwordInput.clear()

def clearRegisterFields():
    firstNameInput.clear()
    lastNameInput.clear()
    registrationEmailInput.clear()
    registrationPasswordInput.clear()
    confirmationPasswordInput.clear()
    
def confirmReservedRental(carID):
    for car in car_data:
        if car[0] == carID and car[1].lower() == "reserved" and car[10] == userData[0]:
            car[1] = "rented"
            saveCarData()
            updateBookingsList()
            showMessage("Success", "Car rental confirmed.")
            mainLayout.setCurrentWidget(bookingWidget)
            return

    showMessage("Error", "Could not confirm rental. Please try again.")




# App Setup
# -------------------------------

app = QApplication(sys.argv)
mainWindow = QWidget()
mainWindow.resize(800, 600)
mainLayout = QStackedLayout()
mainWindow.setLayout(mainLayout)

# Widgets
menuWidget = QWidget()
loginWidget = QWidget()
registerWidget = QWidget()
dashboardWidget = QWidget()
carWidget = QWidget()
bookingWidget = QWidget()
bookingDetailWidget = QWidget()
accountWidget = QWidget()

# Menu Widget
menuLayout = QVBoxLayout(menuWidget)
menuLayout.addWidget(QLabel("Choose an option:"))
loginButton = QPushButton("Login")
registerButton = QPushButton("Register")
menuLayout.addWidget(loginButton)
menuLayout.addWidget(registerButton)

# Login Widget
loginLayout = QVBoxLayout(loginWidget)
loginLayout.addSpacing(75)
emailInput = QLineEdit()
emailInput.setPlaceholderText("Email")
passwordInput = QLineEdit()
passwordInput.setPlaceholderText("Password")
passwordInput.setEchoMode(QLineEdit.Password)
loginSubmit = QPushButton("Submit")
loginBack = QPushButton("Go back")
loginLayout.addWidget(emailInput)
loginLayout.addWidget(passwordInput)
loginLayout.addSpacing(200)
loginLayout.addWidget(loginSubmit)
loginLayout.addWidget(loginBack)

# Register Widget
registerLayout = QVBoxLayout(registerWidget)
firstNameInput = QLineEdit()
firstNameInput.setPlaceholderText("First Name")
lastNameInput = QLineEdit()
lastNameInput.setPlaceholderText("Last Name")
registrationEmailInput = QLineEdit()
registrationEmailInput.setPlaceholderText("Email")
registrationPasswordInput = QLineEdit()
registrationPasswordInput.setPlaceholderText("Password")
registrationPasswordInput.setEchoMode(QLineEdit.Password)
confirmationPasswordInput = QLineEdit()
confirmationPasswordInput.setPlaceholderText("Confirm Password")
confirmationPasswordInput.setEchoMode(QLineEdit.Password)
registerSubmit = QPushButton("Submit")
registerBack = QPushButton("Go back")
registerLayout.addWidget(firstNameInput)
registerLayout.addWidget(lastNameInput)
registerLayout.addWidget(registrationEmailInput)
registerLayout.addWidget(registrationPasswordInput)
registerLayout.addWidget(confirmationPasswordInput)
registerLayout.addSpacing(50)
registerLayout.addWidget(registerSubmit)
registerLayout.addWidget(registerBack)

# Dashboard Widget
dashboardLayout = QVBoxLayout(dashboardWidget)
dashLabel = QLabel("Welcome! Choose an option:")
dashboardLayout.addWidget(dashLabel)
option1 = QPushButton("Browse Cars")
option2_user = QPushButton("View My Bookings")
option2_admin = QPushButton("Manage Users")
option3 = QPushButton("Manage Account")
option4 = QPushButton("Logout")
dashboardLayout.addWidget(option1)
dashboardLayout.addWidget(option2_user)
dashboardLayout.addWidget(option2_admin)
dashboardLayout.addWidget(option3)
dashboardLayout.addWidget(option4)
option2_user.hide()
option2_admin.hide()
debugSpecial = QPushButton("Switch Debug Permissions")

# Car Widget
carLayout = QVBoxLayout(carWidget)
carListDisplay = QListWidget()
carLayout.addWidget(carListDisplay)
bookButton_user = QPushButton("Book Selected Car")
assignButton_admin = QPushButton("Assign Car")
returnButton_admin = QPushButton("Return Car")
carBack = QPushButton("Back to Dashboard")

# Booking Widget
bookingLayout = QVBoxLayout(bookingWidget)
bookingListDisplay = QListWidget()
viewDetailButton = QPushButton("View Car Details")
bookingBack = QPushButton("Back to Dashboard")
bookingLayout.addWidget(bookingListDisplay)
bookingLayout.addWidget(viewDetailButton)
bookingLayout.addWidget(bookingBack)

# Car Details Widget
bookingDetailLayout = QVBoxLayout()
bookingDetailWidget.setLayout(bookingDetailLayout)
bookingCarDetailLabel = QLabel()
confirmRentalButton = QPushButton("Confirm Rental")
confirmRentalButton.hide()
cancelBookingButton = QPushButton("Cancel Booking")
detailBack = QPushButton("Back to My Bookings")
bookingDetailLayout.addWidget(bookingCarDetailLabel)
bookingDetailLayout.addWidget(confirmRentalButton)
bookingDetailLayout.addWidget(cancelBookingButton)
bookingDetailLayout.addWidget(detailBack)
mainLayout.addWidget(bookingDetailWidget)

# Account Widget
accountLayout = QVBoxLayout(accountWidget)
accountInfo = QLabel()
changeEmail = QPushButton("Change Email")
changePasswordButton = QPushButton("Change Password")
managePaymentButton = QPushButton("Manage Payment Details")
deleteAccount = QPushButton("Delete Account")
accountBack = QPushButton("Back to Dashboard")
accountLayout.addWidget(accountInfo)
accountLayout.addWidget(changeEmail)
accountLayout.addWidget(changePasswordButton)
accountLayout.addWidget(managePaymentButton)
accountLayout.addWidget(deleteAccount)
accountLayout.addWidget(accountBack)

# Manage Users Widget
manageUsersWidget = QWidget()
manageUsersLayout = QVBoxLayout(manageUsersWidget)
userListDisplay = QListWidget()
manageUserActionButton = QPushButton("Manage Selected User")
manageUsersBack = QPushButton("Back to Dashboard")
manageUsersLayout.addWidget(userListDisplay)
manageUsersLayout.addWidget(manageUserActionButton)
manageUsersLayout.addWidget(manageUsersBack)



# Main Functions
# -------------------------------

def updateDashboard():
    # Welcome message including the right name
    dashLabel.setText(f"Welcome {userData[1].capitalize()} {userData[2].capitalize()}!")

    # Always show these and reset their labels
    option3.setText("Manage Account")
    option4.setText("Logout")

    # Clear user/admin button position from layout
    if option2_user in [dashboardLayout.itemAt(i).widget() for i in range(dashboardLayout.count())]:
        option2_user.hide()
    if option2_admin in [dashboardLayout.itemAt(i).widget() for i in range(dashboardLayout.count())]:
        option2_admin.hide()

    # Put the buttons in the right place at the right time
    if userData[5] == "true": # Admin
        option1.setText("Manage Cars")
        option2_admin.show()
    else: # User
        option1.setText("Browse Cars")
        option2_user.show()

    # Show this button only for the debug account
    if userData[0] == "0000" and debugSpecial not in [dashboardLayout.itemAt(i).widget() for i in range(dashboardLayout.count())]:
        dashboardLayout.insertWidget(dashboardLayout.count() - 1, debugSpecial)

def updateCarBrowser():
    # Clear the current list
    carListDisplay.clear()

    if userData[5] == "true": # Admin
        # Show all cars with their status
        for car in car_data:
            carListDisplay.addItem(f"{car[0]} | {car[2]} {car[3]} | Status: {car[1]} | Booked by: {car[10]}")
    else: # User
        # Show only available cars
        for car in car_data:
            if car[1].lower() == "available":
                carListDisplay.addItem(f"{car[2]} {car[3]} | {car[9]} Seats | Transmission Type: {car[8]} | {car[5]} per day")


def bookSelectedCar():
    # Looks at the selected car
    selected = carListDisplay.currentRow()
    if selected == -1: # No car selected
        showMessage("Error", "Select a car to rent.")
        return

    # Check if the selected car is available
    availableCars = [car for car in car_data if car[1].lower() == "available"]
    carID = availableCars[selected][0]
    for car in car_data:
        if car[0] == carID:
            car[1] = "reserved"
            car[10] = userData[0]
            break

    # Save the changes, updates the ui and shows a message
    saveCarData()
    updateCarBrowser()
    showMessage("Success", "Car rented successfully!")

def updateBookingsList():
    # Clears the list of cars first
    bookingListDisplay.clear()
    hasBookings = False

    # Adds all of the cars under the users ID and that arent available to the list
    for car in car_data:
        if car[10] == userData[0] and car[1].lower() != "available":
            bookingListDisplay.addItem(
                f"{car[2]} {car[3]} | Car ID: {car[0]} | Status: {car[1]}"
            )
            hasBookings = True

    #if the user doesnt have any bookings it say so in the list
    if not hasBookings:
        bookingListDisplay.addItem("No cars booked.")

def updateCarButtons():
    # Remove all buttons
    carLayout.removeWidget(bookButton_user)
    bookButton_user.hide()
    carLayout.removeWidget(assignButton_admin)
    assignButton_admin.hide()
    carLayout.removeWidget(returnButton_admin)
    returnButton_admin.hide()

    # Add right buttons
    if userData[5] == "true":
        carLayout.addWidget(assignButton_admin)
        assignButton_admin.show()
        carLayout.addWidget(returnButton_admin)
        returnButton_admin.show()
    else:
        carLayout.addWidget(bookButton_user)
        bookButton_user.show()

    # Always show this
    carLayout.addWidget(carBack)
    carBack.show()

def returnSelectedCar():
    # Gets info on selected car in the list
    selected = bookingListDisplay.currentRow()

    # If one isnt selected it returns error message
    if selected == -1:
        showMessage("Error", "Select a car to return.")
        return

    # If the one selected is the no cars booked one then it also sends the error message
    selectedText = bookingListDisplay.item(selected).text()
    if selectedText == "No cars booked.":
        showMessage("Error", "You have no cars to return.")
        return
    
    # Finds all the not available cars that are owned by the user
    ownedCars = [car for car in car_data if car[10] == userData[0] and car[1].lower() != "available"]
    carID = ownedCars[selected][0]

    # Finds the specific car in the list and sets it as available and nolonger in the users posession
    for car in car_data:
        if car[0] == carID:
            car[1] = "available"
            car[10] = ""
            break

    # Saves the list to file and shows returned message
    saveCarData()
    updateBookingsList()
    updateCarBrowser()
    showMessage("Success", "Car returned.")
    
def viewBookCarDetail(index):
    # Hide the rental button to start
    confirmRentalButton.hide()

    # Get all cars booked by this user
    userBookedCars = [car for car in car_data if car[10] == userData[0] and car[1].lower() != "available"]

    # Sends error if the selected car is wrong
    if index >= len(userBookedCars):
        showMessage("Error", "Invalid selection.")
        return

    car = userBookedCars[index]

    # Sets up car detail text
    detailText = (
        f"Car: {car[2]} {car[3]}\n"
        f"Description: {car[8]}\n"
        f"Type: {car[7]}\n"
        f"Seats: {car[9]}\n"
        f"Price per Day: {car[5]}\n"
        f"Status: {car[1].capitalize()}"
    )
    bookingCarDetailLabel.setText(detailText)
    mainLayout.setCurrentWidget(bookingDetailWidget)

    # Rename cancel button depending on the car status
    if car[1].lower() == "rented":
        cancelBookingButton.setText("Return Rental")
    else:
        cancelBookingButton.setText("Cancel Booking")

    # If car is reserved, allow confirming rental 
    if car[1].lower() == "reserved":
        hasPayment = any(p[0].strip() == userData[0].strip() for p in payment_data)
        if hasPayment:
            confirmRentalButton.show()

            # Disconnect previous connections if any
            if confirmRentalButton.receivers(confirmRentalButton.clicked) > 0:
                try:
                    confirmRentalButton.clicked.disconnect()
                except TypeError:
                    pass

            confirmRentalButton.clicked.connect(lambda _, cid=car[0]: confirmReservedRental(cid))
        else: # Only does it if the user has already entered their payment details
            showMessage("Payment Required", "You must add payment details before renting this car.")

def assignSelectedCarToUser():
    # Get the selected row from the car list
    selected = carListDisplay.currentRow()
    
    # If no car is selected show the error message
    if selected == -1:
        showMessage("Error", "Select a car first.")
        return

    # Check if cars only include ones with the available status
    availableCars = [car for car in car_data if car[1].lower() == "available"]
    
    # Sent another error message if the car isnt in the range
    if selected >= len(availableCars):
        showMessage("Error", "Invalid selection.")
        return

    # Get the ID of the selected car and make a list of the users it can be assigned to
    carID = availableCars[selected][0]
    carIndex = next((i for i, c in enumerate(car_data) if c[0] == carID), None)

    # Make the list of eligible users
    eligibleUser = [f"{u[0]} - {u[3]}" for u in user_data if u[5].strip().lower() != "true"]
    
    # If there arent any it shows a error message
    if not eligibleUser:
        showMessage("Error", "No non-admin users available.")
        return

    # Shows a drop down menu of the eligble users
    selectedUser, ok = QInputDialog.getItem(mainWindow, "Assign to User", "Select a user:", eligibleUser, 0, False)
    
    if ok:
        # Get user ID of the selected user
        userID = selectedUser.split(":")[0].strip()
        
        # Update the car data set it as reserved and to the selected user
        car_data[carIndex][1] = "reserved"
        car_data[carIndex][10] = userID
        
        # Save and display the message
        saveCarData()
        updateCarBrowser()
        showMessage("Success", f"Car {carID} assigned to user {userID}.")

def cancelBooking():
    # Get the selected car
    selectedRow = bookingListDisplay.currentRow()
    
    # If nothing is selected give the error message
    if selectedRow == -1:
        showMessage("Error", "Please select a car to cancel.")
        return

    # Make a list of the cars booked or rented by the user
    userBookedCars = []
    for i in range(len(car_data)):
        if car_data[i][1].lower() != "available" and car_data[i][10] == userData[0]:
            userBookedCars.append(i)

    # Make sure that selected row is within the list valid range
    if selectedRow >= len(userBookedCars):
        showMessage("Error", "Invalid selection.")
        return

    # Change the car status, save it and show the message
    carIndex = userBookedCars[selectedRow]
    car_data[carIndex][1] = "available"
    car_data[carIndex][10] = "none"
    saveCarData()
    showMessage("Success", "Booking successfully cancelled!")
    updateBookingsList()
    mainLayout.setCurrentWidget(bookingWidget)

def changeEmailAddress():
    # Stops the debug account from changing their email
    if userData[0] == "0000":
        showMessage("Blocked", "The debug account cannot change its email.")
        return

    # Ask user for a new email address
    newEmail, ok = QInputDialog.getText(mainWindow, "Change Email", "Enter new email:")
    
    # when user entered new email save it and send a message
    if ok and newEmail:
        for i in range(len(user_data)):
            if user_data[i][0] == userData[0]:
                user_data[i][3] = newEmail.lower()
                userData[3] = newEmail
                saveUserData()
                loadAccountInfo()
                showMessage("Success", "Email updated.")
                return

def changePassword():
    # Stops the debug account from changing their password
    if userData[0] == "0000":
        showMessage("Blocked", "The debug account cannot change its password.")
        return

    # Gets the user to enter their current password
    currentPassword, ok1 = QInputDialog.getText(mainWindow, "Verify Password", "Enter current password:")
    
    # If cancelled or incorrect password show the error message and go back
    if not ok1 or currentPassword != userData[4]:
        showMessage("Error", "Password incorrect or cancelled.")
        return

    # ask user for new password
    newPassword, ok2 = QInputDialog.getText(mainWindow, "New Password", "Enter new password:")
    
    # If password is entered and confirmed
    if ok2 and newPassword:
        # Find user ID in user_data
        for i in range(len(user_data)):
            if user_data[i][0] == userData[0]:
                # Update the users password and send a message
                user_data[i][4] = newPassword
                userData[4] = newPassword
                saveUserData()
                showMessage("Success", "Password updated.")
                return
            
def managePaymentDetails():
    global payment_data

    # Get the current users ID
    userID = userData[0]

    # Stop changes on the debug account
    if userID == "0000":
        showMessage("Blocked", "The debug account's payment details cannot be changed.")
        return

    # Check if the user already has payment data
    existingIndex = next((i for i, p in enumerate(payment_data) if p[0] == userID), None)
    
    # Get the users card number 
    number, ok2 = QInputDialog.getText(mainWindow, "Card Number", "Enter 16-digit card number:")
    if not ok2 or not re.fullmatch(r"\d{16}", number):
        showMessage("Invalid Input", "Card number must be 16 digits.")
        return

    # Get the users card expiry date
    expiry, ok3 = QInputDialog.getText(mainWindow, "Expiry Date", "Enter expiry (MM/YY):")
    if not ok3 or not re.fullmatch(r"(0[1-9]|1[0-2])\/\d{2}", expiry):
        showMessage("Invalid Input", "Expiry must be in MM/YY format.")
        return

    # Get the users CVV number
    cvv, ok4 = QInputDialog.getText(mainWindow, "CVV", "Enter 3-digit CVV:")
    if not ok4 or not re.fullmatch(r"\d{3}", cvv):
        showMessage("Invalid Input", "CVV must be 3 digits.")
        return

    # Format the users first and last names
    firstName = userData[1].capitalize()
    lastName = userData[2].capitalize()
    
    # Make a new entery for the users payment detail
    newEntry = [userID, firstName, lastName, number.strip(), expiry.strip(), cvv.strip()]

    # If there is already payment info replace it if not add a new one
    if existingIndex is not None:
        payment_data[existingIndex] = newEntry
    else:
        payment_data = np.append(payment_data, [newEntry], axis=0)

    # Save payment data and a message
    savePaymentData()
    showMessage("Success", "Payment details saved.")

def deleteAccountConfirm():
    global user_data, userData

    # prevents debug account from deleted
    if userData[0] == "0000":
        showMessage("Blocked", "The debug account cannot be deleted.")
        return

    # Check for unreturned cars
    hasRentedCars = any(car[10] == userData[0] and car[1].lower() != "available" for car in car_data)
    if hasRentedCars:
        showMessage("Blocked", "Return all rented cars before deleting your account.")
        return

    # Confirm delete
    confirm, ok = QInputDialog.getText(mainWindow, "Delete Account", "Type DELETE to confirm:")
    if not (ok and confirm.strip().upper() == "DELETE"):
        showMessage("Cancelled", "Account deletion cancelled.")
        return

    # Sets the status of the user as deleted
    for i in range(len(user_data)):
        if user_data[i][0] == userData[0]:
            user_data[i][5] = "deleted"
            break
        
    # Saves the data and shows message
    saveUserData()
    userData = None
    showMessage("Account Deleted", "Your account has been marked as deleted.")
    mainLayout.setCurrentWidget(menuWidget)

def updateUserList():
    # Updates the list of users
    userListDisplay.clear()
    for user in user_data:
        status = user[5].strip().capitalize()
        nameDisplay = f"{user[1]} {user[2]}" if status != "Deleted" else "(Deleted User)"
        userListDisplay.addItem(f"{user[0]} - {nameDisplay} | Status: {status}")

def manageSelectedUser():
    # Gets the selected user
    selected = userListDisplay.currentRow()
    
    # If no user is not selected it displays error message 
    if selected == -1:
        showMessage("Error", "Select a user first.")
        return

    # Gets the data
    userEntry = userListDisplay.item(selected).text()
    userID = userEntry.split(" - ")[0].strip()

    # Prevents any modifying of the debug account
    if userID == "0000":
        showMessage("Blocked", "You cannot modify the debug account.")
        return

    # Stops user from modifying themselfs in this menu
    if userID == userData[0]:
        showMessage("Blocked", "You cannot modify your own account from the admin panel.")
        return

    # finds the user in the user_data list
    index = next((i for i, u in enumerate(user_data) if u[0] == userID), None)

    # if no user data isnt found it displays an error message
    if index is None:
        showMessage("Error", "User not found.")
        return

    # Check if users status is set as deleted
    isDeleted = user_data[index][5].strip().lower() == "deleted"

    # Set the options depending if the user is deleted or not
    if isDeleted:
        options = ["Restore Account"]
    else:
        options = ["Return All Cars", "Toggle Admin", "Delete Account"]

    # show the dialog box with the options above
    choice, ok = QInputDialog.getItem(mainWindow, "Manage User", "Choose an action:", options, 0, False)
    if not ok:
        return

    # Return all the cars
    if choice == "Return All Cars":
        for car in car_data:
            if car[10] == userID and car[1].lower() != "available":
                car[1] = "available"
                car[10] = "none"
        saveCarData()
        showMessage("Success", "All cars returned for user.")

    # Switches the user between admin and normal user permissions
    elif choice == "Toggle Admin":
        current = user_data[index][5].strip().lower()
        user_data[index][5] = "false" if current == "true" else "True"
        saveUserData()
        showMessage("Success", "Admin status updated.")

    # Set the selected users status as deleted, but only iof they dont have any cars booked or rented
    elif choice == "Delete Account":
        hasRented = any(car[10] == userID and car[1].lower() != "available" for car in car_data)
        if hasRented:
            showMessage("Blocked", "User must return all cars before deletion.")
            return
        user_data[index][5] = "deleted"
        saveUserData()
        showMessage("Success", "Account marked as deleted.")
        
    # Sets any deleted account back to normal users
    elif choice == "Restore Account":
        user_data[index][5] = "false"  # Restored users default to non-admin
        saveUserData()
        showMessage("Success", "Account restored.")

    updateUserList()

def loadAccountInfo():
    # Loads acount info
    accountInfo.setText(f"Name: {userData[1].capitalize()} {userData[2].capitalize()}\nEmail: {userData[3]}")

def handleLogin():
    global userData
    
    # Get the email and password
    email = emailInput.text().lower()
    password = passwordInput.text()
    
    # Checks if the user is deleted if it aint then it updates everything for that specific user
    for user in user_data:
        if email == user[3] and password == user[4]:
            if user[5].strip().lower() == "deleted":
                showMessage("Error", "This account has been deleted and cannot be used.")
                clearLoginFields()
                return
            userData = user
            updateDashboard()
            updateCarBrowser()
            mainLayout.setCurrentWidget(dashboardWidget)
            clearLoginFields()
            return
    # If the inputs are invalid output error message
    showMessage("Error", "Invalid login credentials.")
    clearLoginFields()

def handleRegister():
    global user_data

    fname = firstNameInput.text().strip().lower()
    lname = lastNameInput.text().strip().lower()
    email = registrationEmailInput.text().strip().lower()
    password = registrationPasswordInput.text()
    confirmPassword = confirmationPasswordInput.text()

    # Name validation
    if not re.match(r"^[a-zA-Z\s\-]+$", fname):
        showMessage("Invalid Input", "First name must contain only letters, spaces, or hyphens.")
        return
    if not re.match(r"^[a-zA-Z\s\-]+$", lname):
        showMessage("Invalid Input", "Last name must contain only letters, spaces, or hyphens.")
        return

    # Email format check
    if not re.fullmatch(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", email):
        showMessage("Invalid Input", "Invalid email format.")
        return

    # Duplicate email check
    if any(email == user_data[i, 3] for i in range(len(user_data))):
        showMessage("Duplicate Email", "Email already in use.")
        return

    # Password check
    if password != confirmPassword:
        showMessage("Password Error", "Passwords do not match.")
        return

    # Password format check
    if (len(password) < 8 or
        not re.search(r"[A-Z]", password) or
        not re.search(r"[a-z]", password) or
        not re.search(r"\d", password) or
        not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        showMessage("Weak Password", "Password must include at least 8 characters, an uppercase letter, a lowercase letter, a digit, and a special character.")
        return

    # New ID generator
    newID = str(int(user_data[-1, 0]) + 1).zfill(4) if len(user_data) else "0001"
    newUser = [newID, fname, lname, email, password, "False"]
    user_data = np.append(user_data, [newUser], axis=0)

    saveUserData()
    showMessage("Success", "Account created.")
    clearRegisterFields()
    mainLayout.setCurrentWidget(menuWidget)

# Lets the debug account toggle between admin mode
def toggleDebugAdmin():
    global userData
    if userData[5] == "false":
        userData[5] = "true"
        print(f"Switched Debug permissions to admin")
    elif userData[5] == "true":
        userData[5] = "false"
        print(f"Switched Debug permissions to normal")

    updateDashboard()
    mainLayout.setCurrentWidget(dashboardWidget)


# ===============================
# Button Connections
# ===============================
loginButton.clicked.connect(lambda: [clearLoginFields(), mainLayout.setCurrentWidget(loginWidget)])
registerButton.clicked.connect(lambda: [clearRegisterFields(), mainLayout.setCurrentWidget(registerWidget)])
loginSubmit.clicked.connect(handleLogin)
loginBack.clicked.connect(lambda: [mainLayout.setCurrentWidget(menuWidget)])
emailInput.returnPressed.connect(handleLogin)
passwordInput.returnPressed.connect(handleLogin)
registerSubmit.clicked.connect(handleRegister)
registerBack.clicked.connect(lambda: [mainLayout.setCurrentWidget(menuWidget)])
option1.clicked.connect(lambda: [updateCarBrowser(), updateCarButtons(), mainLayout.setCurrentWidget(carWidget)])
option2_user.clicked.connect(lambda: [updateBookingsList(), mainLayout.setCurrentWidget(bookingWidget)])
option2_admin.clicked.connect(lambda: [updateUserList(), mainLayout.setCurrentWidget(manageUsersWidget)])
option3.clicked.connect(lambda: [loadAccountInfo(), mainLayout.setCurrentWidget(accountWidget)])
option4.clicked.connect(lambda: mainLayout.setCurrentWidget(menuWidget))
debugSpecial.clicked.connect(toggleDebugAdmin)
bookButton_user.clicked.connect(bookSelectedCar)
assignButton_admin.clicked.connect(assignSelectedCarToUser)
returnButton_admin.clicked.connect(returnSelectedCar)
changeEmail.clicked.connect(changeEmailAddress)
changePasswordButton.clicked.connect(changePassword)
managePaymentButton.clicked.connect(managePaymentDetails)
deleteAccount.clicked.connect(deleteAccountConfirm)
carBack.clicked.connect(lambda: mainLayout.setCurrentWidget(dashboardWidget))
manageUsersBack.clicked.connect(lambda: mainLayout.setCurrentWidget(dashboardWidget))
manageUserActionButton.clicked.connect(manageSelectedUser)   
bookingBack.clicked.connect(lambda: mainLayout.setCurrentWidget(dashboardWidget))
accountBack.clicked.connect(lambda: mainLayout.setCurrentWidget(dashboardWidget))
viewDetailButton.clicked.connect(lambda: viewBookCarDetail(bookingListDisplay.currentRow()))
detailBack.clicked.connect(lambda: mainLayout.setCurrentWidget(bookingWidget))
cancelBookingButton.clicked.connect(cancelBooking)


# ===============================
# Add and Show
# ===============================
for w in [menuWidget, loginWidget, registerWidget, dashboardWidget,
          carWidget, bookingWidget, accountWidget, manageUsersWidget]:
    mainLayout.addWidget(w)

mainWindow.setWindowTitle("Car Rental System")
mainLayout.setCurrentWidget(menuWidget)
mainWindow.show()
sys.exit(app.exec_())
