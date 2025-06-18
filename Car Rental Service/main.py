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
carFilePath = "Car Rental Service/car_data.csv"

try:
    user_data = np.loadtxt(filePath, delimiter=",", dtype=str)
except Exception as e:
    print(f"Error loading user data: {e}")
    user_data = np.empty((0, 6), dtype=str)

try:
    car_data = np.loadtxt(carFilePath, delimiter=",", dtype=str)
except Exception as e:
    print(f"Error loading car data: {e}")
    car_data = np.empty((0, 11), dtype=str)

userData = None  # Currently logged-in user

# ===============================
# Helper Functions
# ===============================

def save_user_data():
    np.savetxt(filePath, user_data, fmt="%s", delimiter=",")

def save_car_data():
    np.savetxt(carFilePath, car_data, fmt="%s", delimiter=",")

def show_message(title, text):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.exec_()

# ===============================
# Application Setup
# ===============================

app = QApplication(sys.argv)
main_window = QWidget()
main_window.resize(800, 600)
main_layout = QStackedLayout()
main_window.setLayout(main_layout)

# Widgets
menu_widget = QWidget()
login_widget = QWidget()
register_widget = QWidget()
dashboard_widget = QWidget()
car_widget = QWidget()
booking_widget = QWidget()
account_widget = QWidget()

# ===============================
# Menu Widget
# ===============================
menu_layout = QVBoxLayout(menu_widget)
menu_layout.addWidget(QLabel("Choose an option:"))
login_button = QPushButton("Login")
register_button = QPushButton("Register")
menu_layout.addWidget(login_button)
menu_layout.addWidget(register_button)

# ===============================
# Login Widget
# ===============================
login_layout = QVBoxLayout(login_widget)
email_input = QLineEdit()
email_input.setPlaceholderText("Email")
password_input = QLineEdit()
password_input.setPlaceholderText("Password")
password_input.setEchoMode(QLineEdit.Password)
login_submit = QPushButton("Submit")
login_layout.addWidget(email_input)
login_layout.addWidget(password_input)
login_layout.addWidget(login_submit)

# ===============================
# Register Widget
# ===============================
register_layout = QVBoxLayout(register_widget)
fname_input = QLineEdit("First Name")
lname_input = QLineEdit("Last Name")
reg_email_input = QLineEdit("Email")
reg_password_input = QLineEdit("Password")
reg_password_input.setEchoMode(QLineEdit.Password)
confirm_password_input = QLineEdit("Confirm Password")
confirm_password_input.setEchoMode(QLineEdit.Password)
register_submit = QPushButton("Submit")
for w in [fname_input, lname_input, reg_email_input, reg_password_input, confirm_password_input, register_submit]:
    register_layout.addWidget(w)

# ===============================
# Dashboard Widget
# ===============================
dashboard_layout = QVBoxLayout(dashboard_widget)
dash_label = QLabel("Welcome! Choose an option:")
dashboard_layout.addWidget(dash_label)
option1 = QPushButton("Browse Cars")
option2_user = QPushButton("View My Bookings")
option2_admin = QPushButton("Manage Users")
option3 = QPushButton("Manage Account")
option4 = QPushButton("Logout")
for btn in [option1, option3, option4]:
    dashboard_layout.addWidget(btn)

dashboard_layout.addWidget(option2_user)
dashboard_layout.addWidget(option2_admin)
option2_user.hide()
option2_admin.hide()    

debugSpecial = QPushButton("Switch Debug Permissions")

# ===============================
# Car Widget
# ===============================
car_layout = QVBoxLayout(car_widget)
car_list_display = QListWidget()
car_layout.addWidget(car_list_display)
rent_button = QPushButton("Rent Selected Car")
admin_book_button = QPushButton("Book Car")
admin_return_button = QPushButton("Return Car")
back_to_dashboard = QPushButton("Back to Dashboard")

# ===============================
# Booking Widget
# ===============================
booking_layout = QVBoxLayout(booking_widget)
booking_list_display = QListWidget()
return_button = QPushButton("Return Selected Car")
booking_back = QPushButton("Back to Dashboard")
booking_layout.addWidget(booking_list_display)
booking_layout.addWidget(return_button)
booking_layout.addWidget(booking_back)

# ===============================
# Account Widget
# ===============================
account_layout = QVBoxLayout(account_widget)
account_info = QLabel()
change_email = QPushButton("Change Email")
change_pass = QPushButton("Change Password")
delete_account = QPushButton("Delete Account")
account_back = QPushButton("Back to Dashboard")
for w in [account_info, change_email, change_pass, delete_account, account_back]:
    account_layout.addWidget(w)

# ===============================
# Core Functionalities
# ===============================

def update_dashboard():
    dash_label.setText(f"Welcome {userData[1].capitalize()} {userData[2].capitalize()}!")

    # Always show these and reset their labels
    option3.setText("Manage Account")
    option4.setText("Logout")

    # Clear user/admin button position from layout
    if option2_user in [dashboard_layout.itemAt(i).widget() for i in range(dashboard_layout.count())]:
        dashboard_layout.removeWidget(option2_user)
        option2_user.hide()
    if option2_admin in [dashboard_layout.itemAt(i).widget() for i in range(dashboard_layout.count())]:
        dashboard_layout.removeWidget(option2_admin)
        option2_admin.hide()

    # Insert correct button in consistent position (3rd place)
    if userData[5] == "true":
        option1.setText("Manage Cars")
        dashboard_layout.insertWidget(2, option2_admin)
        option2_admin.show()
    else:
        option1.setText("Browse Cars")
        dashboard_layout.insertWidget(2, option2_user)
        option2_user.show()

    # Ensure debug switch is last (before Logout)
    if userData[0] == "0000" and debugSpecial not in [dashboard_layout.itemAt(i).widget() for i in range(dashboard_layout.count())]:
        dashboard_layout.insertWidget(dashboard_layout.count() - 1, debugSpecial)



def update_car_list():
    car_list_display.clear()
    if userData[5] == "true":
        for car in car_data:
            car_list_display.addItem(f"{car[0]} - {car[2]} {car[3]} | {car[5]} per day | Status: {car[1]}")
    else:
        for car in car_data:
            if car[1].lower() == "available":
                car_list_display.addItem(f"{car[0]} - {car[2]} {car[3]} | {car[5]} per day")


def rent_selected_car():
    selected = car_list_display.currentRow()
    if selected == -1:
        show_message("Error", "Select a car to rent.")
        return
    available_cars = [car for car in car_data if car[1].lower() == "available"]
    car_id = available_cars[selected][0]
    for car in car_data:
        if car[0] == car_id:
            car[1] = "Unavailable"
            car[10] = userData[0]
            break
    save_car_data()
    update_car_list()
    show_message("Success", "Car rented successfully!")

def update_booking_list():
    booking_list_display.clear()
    has_bookings = False

    for car in car_data:
        if car[10] == userData[0] and car[1].lower() == "unavailable":
            booking_list_display.addItem(f"{car[0]} - {car[2]} {car[3]} | {car[5]} per day")
            has_bookings = True

    if not has_bookings:
        booking_list_display.addItem("No cars booked.")


def update_car_buttons():
    # Remove all current action buttons first
    car_layout.removeWidget(rent_button)
    rent_button.hide()
    car_layout.removeWidget(admin_book_button)
    admin_book_button.hide()
    car_layout.removeWidget(admin_return_button)
    admin_return_button.hide()

    # Add appropriate buttons
    if userData[5] == "true":
        car_layout.addWidget(admin_book_button)
        admin_book_button.show()
        car_layout.addWidget(admin_return_button)
        admin_return_button.show()
    else:
        car_layout.addWidget(rent_button)
        rent_button.show()
    
    # Always show this
    car_layout.addWidget(back_to_dashboard)
    back_to_dashboard.show()

def return_selected_car():
    selected = booking_list_display.currentRow()

    if selected == -1:
        show_message("Error", "Select a car to return.")
        return

    selected_text = booking_list_display.item(selected).text()
    if selected_text == "No cars booked.":
        show_message("Error", "You have no cars to return.")
        return

    owned_cars = [car for car in car_data if car[10] == userData[0] and car[1].lower() == "unavailable"]
    car_id = owned_cars[selected][0]

    for car in car_data:
        if car[0] == car_id:
            car[1] = "Available"
            car[10] = ""
            break

    save_car_data()
    update_booking_list()
    update_car_list()
    show_message("Success", "Car returned.")


def load_account_info():
    account_info.setText(f"Name: {userData[1].capitalize()} {userData[2].capitalize()}\nEmail: {userData[3]}")

def handle_login():
    global userData
    email = email_input.text().lower()
    password = password_input.text()
    for user in user_data:
        if email == user[3] and password == user[4]:
            userData = user
            update_dashboard()
            update_car_list()
            main_layout.setCurrentWidget(dashboard_widget)
            return
    show_message("Error", "Invalid login credentials.")

def handle_register():
    global user_data
    fname = fname_input.text().strip().lower()
    lname = lname_input.text().strip().lower()
    email = reg_email_input.text().strip().lower()
    password = reg_password_input.text()
    confirm_password = confirm_password_input.text()
    if password != confirm_password:
        show_message("Error", "Passwords do not match.")
        return
    new_id = str(int(user_data[-1][0]) + 1).zfill(4) if len(user_data) else "0001"
    new_user = [new_id, fname, lname, email, password, "False"]
    user_data = np.append(user_data, [new_user], axis=0)
    save_user_data()
    show_message("Success", "Account created.")
    main_layout.setCurrentWidget(menu_widget)

def toggle_debug_admin():
    global userData
    if userData[5] == "false":
        userData[5] = "true"
        print(f"Switched Debug permissions to admin")
    elif userData[5] == "true":
        userData[5] = "false"
        print(f"Switched Debug permissions to normal")

    update_dashboard()
    main_layout.setCurrentWidget(dashboard_widget)


# ===============================
# Button Connections
# ===============================
login_button.clicked.connect(lambda: main_layout.setCurrentWidget(login_widget))
register_button.clicked.connect(lambda: main_layout.setCurrentWidget(register_widget))
login_submit.clicked.connect(handle_login)
register_submit.clicked.connect(handle_register)
option1.clicked.connect(lambda: [update_car_list(), update_car_buttons(), main_layout.setCurrentWidget(car_widget)])
option2_user.clicked.connect(lambda: [update_booking_list(), main_layout.setCurrentWidget(booking_widget)])
option2_admin.clicked.connect(lambda: show_message("Admin", "Manage Users clicked."))
option3.clicked.connect(lambda: [load_account_info(), main_layout.setCurrentWidget(account_widget)])
option4.clicked.connect(lambda: main_layout.setCurrentWidget(menu_widget))
debugSpecial.clicked.connect(toggle_debug_admin)
rent_button.clicked.connect(rent_selected_car)
admin_book_button.clicked.connect(lambda: show_message("Admin", "Book Car clicked."))
admin_return_button.clicked.connect(lambda: show_message("Admin", "Return Car clicked."))
back_to_dashboard.clicked.connect(lambda: main_layout.setCurrentWidget(dashboard_widget))
return_button.clicked.connect(return_selected_car)
booking_back.clicked.connect(lambda: main_layout.setCurrentWidget(dashboard_widget))
account_back.clicked.connect(lambda: main_layout.setCurrentWidget(dashboard_widget))

# ===============================
# Add and Show
# ===============================
for w in [menu_widget, login_widget, register_widget, dashboard_widget,
          car_widget, booking_widget, account_widget]:
    main_layout.addWidget(w)

main_window.setWindowTitle("Car Rental System")
main_layout.setCurrentWidget(menu_widget)
main_window.show()
sys.exit(app.exec_())
