# Full Version of Cleaned Car Rental Application with Dashboard, Admin, and Booking

import sys
import numpy as np
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QLineEdit, QMessageBox, QStackedLayout, QHBoxLayout, QListWidget, QInputDialog
)

# ===============================
# Data Loading and Initialization
# ===============================

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

userData = None  # Currently logged-in user

# ===============================
# Helper Functions
# ===============================

def saveUserData():
    np.savetxt(filePath, user_data, fmt="%s", delimiter=",")

def saveCarData():
    np.savetxt(filePath, car_data, fmt="%s", delimiter=",")

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


# ===============================
# Application Setup
# ===============================

app = QApplication(sys.argv)
mainWindow = QWidget()
mainWindow.resize(800, 600)
mainLayout = QStackedLayout()
mainWindow.setLayout(mainLayout)

# Widgets
menuWidget = QWidget()
loginWidget = QWidget()
registerWidget = QWidget()
dashboard_widget = QWidget()
carWidget = QWidget()
bookingWidget = QWidget()
accountWidget = QWidget()

# ===============================
# Menu Widget
# ===============================
menuWidget = QVBoxLayout(menuWidget)
menuWidget.addWidget(QLabel("Choose an option:"))
loginWidget = QPushButton("Login")
registerWidget = QPushButton("Register")
menuWidget.addWidget(loginWidget)
menuWidget.addWidget(registerWidget)

# ===============================
# Login Widget
# ===============================
loginWidget = QVBoxLayout(loginWidget)
emailInput = QLineEdit()
emailInput.setPlaceholderText("Email")
passwordInput = QLineEdit()
passwordInput.setPlaceholderText("Password")
passwordInput.setEchoMode(QLineEdit.Password)
loginSubmit = QPushButton("Submit")
loginWidget.addWidget(emailInput)
loginWidget.addWidget(passwordInput)
loginWidget.addWidget(loginSubmit)


# ===============================
# Register Widget
# ===============================
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
for w in [firstNameInput, lastNameInput, registrationEmailInput, registrationPasswordInput, confirmationPasswordInput, registerSubmit]:
    registerLayout.addWidget(w)

# ===============================
# Dashboard Widget
# ===============================
dashboardLayout = QVBoxLayout(dashboard_widget)
dashLabel = QLabel("Welcome! Choose an option:")
dashboardLayout.addWidget(dashLabel)
option1 = QPushButton("Browse Cars")
option2_user = QPushButton("View My Bookings")
option2_admin = QPushButton("Manage Users")
option3 = QPushButton("Manage Account")
option4 = QPushButton("Logout")
for btn in [option1, option3, option4]:
    dashboardLayout.addWidget(btn)

dashboardLayout.addWidget(option2_user)
dashboardLayout.addWidget(option2_admin)
option2_user.hide()
option2_admin.hide()

debugSpecial = QPushButton("Switch Debug Permissions")

# ===============================
# Car Widget
# ===============================
carLayout = QVBoxLayout(carWidget)
carListDisplay = QListWidget()
carLayout.addWidget(carListDisplay)
rentButton_admin = QPushButton("Rent Selected Car")
assignButton_admin = QPushButton("Assign Car")
returnButton_admin = QPushButton("Return Car")
carBack = QPushButton("Back to Dashboard")

# ===============================
# Booking Widget
# ===============================
bookingLayout = QVBoxLayout(bookingWidget)
bookingListDisplay = QListWidget()
returnButton = QPushButton("Return Selected Car")
bookingBack = QPushButton("Back to Dashboard")
bookingLayout.addWidget(bookingListDisplay)
bookingLayout.addWidget(returnButton)
bookingLayout.addWidget(bookingBack)

# ===============================
# Account Widget
# ===============================
accountLayout = QVBoxLayout(accountWidget)
accountInfo = QLabel()
changeEmail = QPushButton("Change Email")
changePass = QPushButton("Change Password")
deleteAccount = QPushButton("Delete Account")
accountBack = QPushButton("Back to Dashboard")
for w in [accountInfo, changeEmail, changePass, deleteAccount, accountBack]:
    accountLayout.addWidget(w)

# ===============================
# Manage Users Widget
# ===============================

manageUsersWidget = QWidget()
manageUsersLayout = QVBoxLayout(manageUsersWidget)

userListDisplay = QListWidget()
manageUserActionButton = QPushButton("Manage Selected User")
usersBack = QPushButton("Back to Dashboard")

manageUsersLayout.addWidget(userListDisplay)
manageUsersLayout.addWidget(manageUserActionButton)
manageUsersLayout.addWidget(usersBack)



# Main Functions
# -------------------------------

# Update Menus
def updateDashboard():
    # Welcome message including the right name
    dashLabel.setText(f"Welcome {userData[1].capitalize()} {userData[2].capitalize()}!")

    # Always show these and reset their labels
    option3.setText("Manage Account")
    option4.setText("Logout")

    # Clear user/admin button position from layout
    if option2_user in [dashboardLayout.itemAt(i).widget() for i in range(dashboardLayout.count())]:
        dashboardLayout.removeWidget(option2_user)
        option2_user.hide()
    if option2_admin in [dashboardLayout.itemAt(i).widget() for i in range(dashboardLayout.count())]:
        dashboardLayout.removeWidget(option2_admin)
        option2_admin.hide()

    # Put the buttons in the right place at the right time
    if userData[5] == "true": # Admin
        option1.setText("Manage Cars")
        dashboardLayout.insertWidget(2, option2_admin)
        option2_admin.show()
    else: # User
        option1.setText("Browse Cars")
        dashboardLayout.insertWidget(2, option2_user)
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
            carListDisplay.addItem(f"{car[0]} - {car[2]} {car[3]} | {car[5]} per day | Status: {car[1]}")
    else: # User
        # Show only available cars
        for car in car_data:
            if car[1].lower() == "available":
                carListDisplay.addItem(f"{car[0]} - {car[2]} {car[3]} | {car[5]} per day")

def updateBookingsList():
    bookingListDisplay.clear()
    hasBookings = False

    for car in car_data:
        if car[10] == userData[0] and car[1].lower() == "unavailable":
            bookingListDisplay.addItem(f"{car[0]} - {car[2]} {car[3]} | {car[5]} per day")
            hasBookings = True

    if not hasBookings:
        bookingListDisplay.addItem("No cars booked.")

def updateCarButtons():
    # Remove all current action buttons first
    carLayout.removeWidget(rentButton_admin)
    rentButton_admin.hide()
    carLayout.removeWidget(assignButton_admin)
    assignButton_admin.hide()
    carLayout.removeWidget(returnButton_admin)
    returnButton_admin.hide()

    # Add appropriate buttons
    if userData[5] == "true":
        carLayout.addWidget(assignButton_admin)
        assignButton_admin.show()
        carLayout.addWidget(returnButton_admin)
        returnButton_admin.show()
    else:
        carLayout.addWidget(rentButton_admin)
        rentButton_admin.show()

    # Always show this
    carLayout.addWidget(carBack)
    carBack.show()

def updateUserList():
    userListDisplay.clear()
    for user in user_data:
        status = user[5].strip().capitalize()
        nameDisplay = f"{user[1]} {user[2]}" if status != "Deleted" else "(Deleted User)"
        userListDisplay.addItem(f"{user[0]} - {nameDisplay} | Status: {status}")

# Load account info + login
def loadAccountInfo():
    accountInfo.setText(f"Name: {userData[1].capitalize()} {userData[2].capitalize()}\nEmail: {userData[3]}")

def handleLogin():
    global userData
    email = emailInput.text().lower()
    password = passwordInput.text()
    for user in user_data:
        if email == user[3] and password == user[4]:
            if user[5].strip().lower() == "deleted":
                showMessage("Error", "This account has been deleted and cannot be used.")
                clearLoginFields()
                return
            userData = user
            updateDashboard()
            updateCarBrowser()
            mainLayout.setCurrentWidget(dashboard_widget)
            clearLoginFields()
            return
    showMessage("Error", "Invalid login credentials.")
    clearLoginFields()




def rentSelectedCar():
    # Looks at the selected car
    selected = carListDisplay.currentRow()
    if selected == -1: # No car selected
        showMessage("Error", "Select a car to rent.")
        return

    # Check if the selected car is available
    available_cars = [car for car in car_data if car[1].lower() == "available"]
    car_id = available_cars[selected][0]
    for car in car_data:
        if car[0] == car_id:
            car[1] = "Unavailable"
            car[10] = userData[0]
            break

    # Save the changes, updates the ui and shows a message
    saveCarData()
    updateCarBrowser()
    showMessage("Success", "Car rented successfully!")

def returnSelectedCar():
    selected = bookingListDisplay.currentRow()

    if selected == -1:
        showMessage("Error", "Select a car to return.")
        return

    selected_text = bookingListDisplay.item(selected).text()
    if selected_text == "No cars booked.":
        showMessage("Error", "You have no cars to return.")
        return

    owned_cars = [car for car in car_data if car[10] == userData[0] and car[1].lower() == "unavailable"]
    car_id = owned_cars[selected][0]

    for car in car_data:
        if car[0] == car_id:
            car[1] = "available"
            car[10] = ""
            break

    saveCarData()
    updateBookingsList()
    updateCarBrowser()
    showMessage("Success", "Car returned.")

def assignSelectedCarToUser():
    selected = carListDisplay.currentRow()
    if selected == -1:
        showMessage("Error", "Select a car first.")
        return

    available_cars = [car for car in car_data if car[1].lower() == "available"]
    if selected >= len(available_cars):
        showMessage("Error", "Invalid selection.")
        return

    car_id = available_cars[selected][0]
    car_idx = next((i for i, c in enumerate(car_data) if c[0] == car_id), None)

    eligible_users = [f"{u[0]} - {u[3]}" for u in user_data if u[5].strip().lower() != "true"]
    if not eligible_users:
        showMessage("Error", "No non-admin users available.")
        return

    selected_user, ok = QInputDialog.getItem(mainWindow, "Assign to User", "Select a user:", eligible_users, 0, False)
    if ok:
        user_id = selected_user.split(":")[0].strip()
        car_data[car_idx][1] = "Unavailable"
        car_data[car_idx][10] = user_id
        saveCarData()
        updateCarBrowser()
        showMessage("Success", f"Car {car_id} assigned to user {user_id}.")

def returnSelectedCar():
    selected = carListDisplay.currentRow()
    if selected == -1:
        showMessage("Error", "Select a car first.")
        return

    # Show only cars that are unavailable
    unavailable_cars = [car for car in car_data if car[1].lower() == "unavailable"]
    if selected >= len(unavailable_cars):
        showMessage("Error", "Invalid selection.")
        return

    car_id = unavailable_cars[selected][0]
    car_idx = next((i for i, c in enumerate(car_data) if c[0] == car_id), None)

    if car_idx is not None:
        car_data[car_idx][1] = "available"
        car_data[car_idx][10] = ""  # clear assigned user
        saveCarData()
        updateCarBrowser()
        showMessage("Success", f"Car {car_id} returned and marked available.")

def changeEmailAddress():
    if userData[0] == "0000":
        showMessage("Blocked", "The debug account cannot change its email.")
        return

    new_email, ok = QInputDialog.getText(mainWindow, "Change Email", "Enter new email:")
    if ok and new_email:
        for i in range(len(user_data)):
            if user_data[i][0] == userData[0]:
                user_data[i][3] = new_email
                userData[3] = new_email  # sync session
                saveUserData()
                loadAccountInfo()
                showMessage("Success", "Email updated.")
                return

def changePassword():
    if userData[0] == "0000":
        showMessage("Blocked", "The debug account cannot change its password.")
        return

    current_password, ok1 = QInputDialog.getText(mainWindow, "Verify Password", "Enter current password:")
    if not ok1 or current_password != userData[4]:
        showMessage("Error", "Password incorrect or cancelled.")
        return

    new_password, ok2 = QInputDialog.getText(mainWindow, "New Password", "Enter new password:")
    if ok2 and new_password:
        for i in range(len(user_data)):
            if user_data[i][0] == userData[0]:
                user_data[i][4] = new_password
                userData[4] = new_password  # sync session
                saveUserData()
                showMessage("Success", "Password updated.")
                return

def deleteAccountConfirm():
    global user_data, userData

    if userData[0] == "0000":
        showMessage("Blocked", "The debug account cannot be deleted.")
        return

    # Check for unreturned cars
    has_rented_cars = any(car[10] == userData[0] and car[1].lower() == "unavailable" for car in car_data)
    if has_rented_cars:
        showMessage("Blocked", "Return all rented cars before deleting your account.")
        return

    # Confirm delete
    confirm, ok = QInputDialog.getText(mainWindow, "Delete Account", "Type DELETE to confirm:")
    if not (ok and confirm.strip().upper() == "DELETE"):
        showMessage("Cancelled", "Account deletion cancelled.")
        return

    # Soft-delete: mark first and last name
    for i in range(len(user_data)):
        if user_data[i][0] == userData[0]:
            user_data[i][5] = "deleted"  # Mark as deleted (custom flag)
            break

    saveUserData()
    userData = None
    showMessage("Account Deleted", "Your account has been marked as deleted.")
    mainLayout.setCurrentWidget(menuWidget)

def manageSelectedUser():
    selected = userListDisplay.currentRow()
    if selected == -1:
        showMessage("Error", "Select a user first.")
        return

    user_entry = userListDisplay.item(selected).text()
    user_id = user_entry.split(" - ")[0].strip()

    if user_id == "0000":
        showMessage("Blocked", "You cannot modify the debug account.")
        return

    if user_id == userData[0]:
        showMessage("Blocked", "You cannot modify your own account from the admin panel.")
        return

    idx = next((i for i, u in enumerate(user_data) if u[0] == user_id), None)

    if idx is None:
        showMessage("Error", "User not found.")
        return

    is_deleted = user_data[idx][5].strip().lower() == "deleted"

    if is_deleted:
        options = ["Restore Account"]
    else:
        options = ["Return All Cars", "Toggle Admin", "Delete Account"]

    choice, ok = QInputDialog.getItem(mainWindow, "Manage User", "Choose an action:", options, 0, False)
    if not ok:
        return

    if choice == "Return All Cars":
        for car in car_data:
            if car[10] == user_id and car[1].lower() == "unavailable":
                car[1] = "available"
                car[10] = ""
        saveCarData()
        showMessage("Success", "All cars returned for user.")

    elif choice == "Toggle Admin":
        current = user_data[idx][5].strip().lower()
        user_data[idx][5] = "false" if current == "true" else "True"
        saveUserData()
        showMessage("Success", "Admin status updated.")

    elif choice == "Delete Account":
        has_rented = any(car[10] == user_id and car[1].lower() == "unavailable" for car in car_data)
        if has_rented:
            showMessage("Blocked", "User must return all cars before deletion.")
            return
        user_data[idx][5] = "deleted"
        saveUserData()
        showMessage("Success", "Account marked as deleted.")

    elif choice == "Restore Account":
        user_data[idx][5] = "false"  # Restored users default to non-admin
        saveUserData()
        showMessage("Success", "Account restored.")

    updateUserList()

def handleRegister():
    global user_data

    fname = firstNameInput.text().strip().lower()
    lname = lastNameInput.text().strip().lower()
    email = registrationEmailInput.text().strip().lower()
    password = registrationPasswordInput.text()
    confirm_password = confirmationPasswordInput.text()

    # === Name validation
    if not re.match(r"^[a-zA-Z\s\-]+$", fname):
        showMessage("Invalid Input", "First name must contain only letters, spaces, or hyphens.")
        return
    if not re.match(r"^[a-zA-Z\s\-]+$", lname):
        showMessage("Invalid Input", "Last name must contain only letters, spaces, or hyphens.")
        return

    # === Email format
    if not re.fullmatch(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", email):
        showMessage("Invalid Input", "Invalid email format.")
        return

    # === Duplicate email check
    if any(email == user_data[i, 3] for i in range(len(user_data))):
        showMessage("Duplicate Email", "Email already in use.")
        return

    # === Password checks
    if password != confirm_password:
        showMessage("Password Error", "Passwords do not match.")
        return

    if (len(password) < 8 or
        not re.search(r"[A-Z]", password) or
        not re.search(r"[a-z]", password) or
        not re.search(r"\d", password) or
        not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        showMessage("Weak Password", "Password must include at least 8 characters, an uppercase letter, a lowercase letter, a digit, and a special character.")
        return

    # === New ID generation
    new_id = str(int(user_data[-1, 0]) + 1).zfill(4) if len(user_data) else "0001"
    new_user = [new_id, fname, lname, email, password, "False"]
    user_data = np.append(user_data, [new_user], axis=0)

    saveUserData()
    showMessage("Success", "Account created.")
    clearRegisterFields()
    mainLayout.setCurrentWidget(menuWidget)

def toggleDebugAdmin():
    global userData
    if userData[5] == "false":
        userData[5] = "true"
        print(f"Switched Debug permissions to admin")
    elif userData[5] == "true":
        userData[5] = "false"
        print(f"Switched Debug permissions to normal")

    updateDashboard()
    mainLayout.setCurrentWidget(dashboard_widget)


# ===============================
# Button Connections
# ===============================
loginWidget.clicked.connect(lambda: [clearLoginFields(), mainLayout.setCurrentWidget(loginWidget)])
registerWidget.clicked.connect(lambda: [clearRegisterFields(), mainLayout.setCurrentWidget(registerWidget)])
loginSubmit.clicked.connect(handleLogin)
emailInput.returnPressed.connect(handleLogin)
passwordInput.returnPressed.connect(handleLogin)
registerSubmit.clicked.connect(handleRegister)
option1.clicked.connect(lambda: [updateCarBrowser(), updateCarButtons(), mainLayout.setCurrentWidget(carWidget)])
option2_user.clicked.connect(lambda: [updateBookingsList(), mainLayout.setCurrentWidget(bookingWidget)])
option2_admin.clicked.connect(lambda: [updateUserList(), mainLayout.setCurrentWidget(manageUsersWidget)])
option3.clicked.connect(lambda: [loadAccountInfo(), mainLayout.setCurrentWidget(accountWidget)])
option4.clicked.connect(lambda: mainLayout.setCurrentWidget(menuWidget))
debugSpecial.clicked.connect(toggleDebugAdmin)
rentButton_admin.clicked.connect(rentSelectedCar)
assignButton_admin.clicked.connect(assignSelectedCarToUser)
returnButton_admin.clicked.connect(returnSelectedCar)
changeEmail.clicked.connect(changeEmailAddress)
changePass.clicked.connect(changePassword)
deleteAccount.clicked.connect(deleteAccountConfirm)
carBack.clicked.connect(lambda: mainLayout.setCurrentWidget(dashboard_widget))
usersBack.clicked.connect(lambda: mainLayout.setCurrentWidget(dashboard_widget))
manageUserActionButton.clicked.connect(manageSelectedUser)
returnButton.clicked.connect(returnSelectedCar)
bookingBack.clicked.connect(lambda: mainLayout.setCurrentWidget(dashboard_widget))
accountBack.clicked.connect(lambda: mainLayout.setCurrentWidget(dashboard_widget))


# ===============================
# Add and Show
# ===============================
for w in [menuWidget, loginWidget, registerWidget, dashboard_widget,
          carWidget, bookingWidget, accountWidget, manageUsersWidget]:
    mainLayout.addWidget(w)

mainWindow.setWindowTitle("Car Rental System")
mainLayout.setCurrentWidget(menuWidget)
mainWindow.show()
sys.exit(app.exec_())
