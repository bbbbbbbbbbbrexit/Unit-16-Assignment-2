import sys
import numpy as np
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel,
    QLineEdit, QMessageBox, QStackedLayout, QHBoxLayout, QListWidget, QInputDialog
)

# Load user data
filePath = "Car Rental Service/user_data.csv"
user_data = np.loadtxt(filePath, delimiter=",", dtype=str, skiprows=1)
userData = None

# Load car data
carFilePath = "Car Rental Service/car_data.csv"
car_data = np.loadtxt(carFilePath, delimiter=",", dtype=str, skiprows=1)
carList = []
for i in range(len(car_data)):
    if car_data[i][1].lower() == "unavailable":
        continue
    carEntry = [
        str(car_data[i][0]),
        str(car_data[i][2]),
        str(car_data[i][3]),
        str(car_data[i][8]),
        str(car_data[i][7]),
        str(car_data[i][9]),
        str(car_data[i][5])
    ]
    carList.append(carEntry)

def save_user_data():
    np.savetxt(filePath, user_data, fmt="%s", delimiter=",")

def save_car_data():
    np.savetxt(carFilePath, car_data, fmt="%s", delimiter=",")

def show_message(title, text):
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.exec_()

app = QApplication(sys.argv)

main_window = QWidget()
main_window.resize(800, 600)
main_layout = QStackedLayout()
main_window.setLayout(main_layout)

# Login/Register Menu
menu_widget = QWidget()
menu_layout = QVBoxLayout()
menu_widget.setLayout(menu_layout)
menu_label = QLabel("Choose an option:")
login_button = QPushButton("Login")
register_button = QPushButton("Register")
menu_layout.addWidget(menu_label)
menu_layout.addWidget(login_button)
menu_layout.addWidget(register_button)

# Login Widget
login_widget = QWidget()
login_layout = QVBoxLayout()
login_widget.setLayout(login_layout)
email_input = QLineEdit()
email_input.setPlaceholderText("Email")
password_input = QLineEdit()
password_input.setPlaceholderText("Password")
password_input.setEchoMode(QLineEdit.Password)
login_submit = QPushButton("Submit")
login_layout.addWidget(email_input)
login_layout.addWidget(password_input)
login_layout.addWidget(login_submit)

# Register Widget
register_widget = QWidget()
register_layout = QVBoxLayout()
register_widget.setLayout(register_layout)
fname_input = QLineEdit()
fname_input.setPlaceholderText("First Name")
lname_input = QLineEdit()
lname_input.setPlaceholderText("Last Name")
reg_email_input = QLineEdit()
reg_email_input.setPlaceholderText("Email")
reg_password_input = QLineEdit()
reg_password_input.setPlaceholderText("Password")
reg_password_input.setEchoMode(QLineEdit.Password)
confirm_password_input = QLineEdit()
confirm_password_input.setPlaceholderText("Confirm Password")
confirm_password_input.setEchoMode(QLineEdit.Password)
register_submit = QPushButton("Submit")
register_layout.addWidget(fname_input)
register_layout.addWidget(lname_input)
register_layout.addWidget(reg_email_input)
register_layout.addWidget(reg_password_input)
register_layout.addWidget(confirm_password_input)
register_layout.addWidget(register_submit)

# User Dashboard
dashboard_widget = QWidget()
dash_layout = QVBoxLayout()
dashboard_widget.setLayout(dash_layout)
dash_label = QLabel("Welcome! Choose an option:")
option1 = QPushButton("Browse Cars for Rent")
option2 = QPushButton("Manage Bookings")
option3 = QPushButton("Manage your Account")
option4 = QPushButton("Exit")
dash_layout.addWidget(dash_label)
dash_layout.addWidget(option1)
dash_layout.addWidget(option2)
dash_layout.addWidget(option3)
dash_layout.addWidget(option4)

# Car Browsing Widget
car_widget = QWidget()
car_layout = QVBoxLayout()
car_widget.setLayout(car_layout)

car_list_display = QListWidget()
car_layout.addWidget(car_list_display)

pagination_layout = QHBoxLayout()
prev_button = QPushButton("Previous")
next_button = QPushButton("Next")
back_button = QPushButton("Back to Dashboard")
pagination_layout.addWidget(prev_button)
pagination_layout.addWidget(next_button)
pagination_layout.addWidget(back_button)
car_layout.addLayout(pagination_layout)

# Car Detail Widget
car_detail_widget = QWidget()
car_detail_layout = QVBoxLayout()
car_detail_widget.setLayout(car_detail_layout)

car_detail_label = QLabel()
rent_button = QPushButton("Rent this Car")
back_to_list_button = QPushButton("Back to Car List")

car_detail_layout.addWidget(car_detail_label)
car_detail_layout.addWidget(rent_button)
car_detail_layout.addWidget(back_to_list_button)

# Manage Bookings Widget
booking_widget = QWidget()
booking_layout = QVBoxLayout()
booking_widget.setLayout(booking_layout)

booking_list_display = QListWidget()
booking_layout.addWidget(booking_list_display)

booking_button_layout = QHBoxLayout()
return_button = QPushButton("Return Selected Car")
back_to_dashboard_button = QPushButton("Back to Dashboard")
booking_button_layout.addWidget(return_button)
booking_button_layout.addWidget(back_to_dashboard_button)
booking_layout.addLayout(booking_button_layout)

# Manage Account Widget
account_widget = QWidget()
account_layout = QVBoxLayout()
account_widget.setLayout(account_layout)

account_info_label = QLabel()
change_email_button = QPushButton("Change Email")
change_password_button = QPushButton("Change Password")
delete_account_button = QPushButton("Delete Account")
account_back_button = QPushButton("Back to Dashboard")

account_layout.addWidget(account_info_label)
account_layout.addWidget(change_email_button)
account_layout.addWidget(change_password_button)
account_layout.addWidget(delete_account_button)
account_layout.addWidget(account_back_button)

# Add widgets to main layout
main_layout.addWidget(menu_widget)
main_layout.addWidget(login_widget)
main_layout.addWidget(register_widget)
main_layout.addWidget(dashboard_widget)
main_layout.addWidget(car_widget)
main_layout.addWidget(car_detail_widget)
main_layout.addWidget(booking_widget)
main_layout.addWidget(account_widget)

# Pagination Logic
current_page = [1]
cars_per_page = 10
selected_car_index = [None]

def update_car_list():
    car_list_display.clear()
    start = (current_page[0] - 1) * cars_per_page
    end = min(start + cars_per_page, len(carList))
    for i in range(start, end):
        car = carList[i]
        display_text = f"{car[1]} {car[2]} | {car[3]} | {car[4]} | {car[5]} Seats | {car[6]} per day"
        car_list_display.addItem(display_text)

def next_page():
    if current_page[0] * cars_per_page < len(carList):
        current_page[0] += 1
        update_car_list()
    else:
        show_message("Info", "You are on the last page.")

def prev_page():
    if current_page[0] > 1:
        current_page[0] -= 1
        update_car_list()
    else:
        show_message("Info", "You are on the first page.")

def view_car_detail(index):
    selected_car_index[0] = (current_page[0] - 1) * cars_per_page + index
    car = carList[selected_car_index[0]]
    detail_text = (
        f"Car: {car[1]} {car[2]}\n"
        f"Description: {car[3]}\n"
        f"Type: {car[4]}\n"
        f"Seats: {car[5]}\n"
        f"Price per Day: {car[6]}"
    )
    car_detail_label.setText(detail_text)
    main_layout.setCurrentWidget(car_detail_widget)

def rent_selected_car():
    if selected_car_index[0] is not None:
        car_id = carList[selected_car_index[0]][0]

        # Mark the car as unavailable and assign user ID
        for i in range(len(car_data)):
            if car_data[i][0] == car_id:
                car_data[i][1] = "Unavailable"
                car_data[i][10] = userData[0]  # Assign the user ID
                break

        save_car_data()

        # Remove from available list
        carList.pop(selected_car_index[0])

        show_message("Success", "Car successfully rented!")
        update_car_list()
        main_layout.setCurrentWidget(car_widget)

def update_booking_list():
    booking_list_display.clear()
    for i in range(len(car_data)):
        if car_data[i][1].lower() == "unavailable" and car_data[i][10] == userData[0]:
            display_text = f"{car_data[i][2]} {car_data[i][3]} | {car_data[i][8]} | {car_data[i][7]} | {car_data[i][9]} Seats | {car_data[i][5]} per day | Car ID: {car_data[i][0]}"
            booking_list_display.addItem(display_text)

def return_selected_car():
    selected_row = booking_list_display.currentRow()
    if selected_row == -1:
        show_message("Error", "Please select a car to return.")
        return

    user_booked_cars = []
    for i in range(len(car_data)):
        if car_data[i][1].lower() == "unavailable" and car_data[i][10] == userData[0]:
            user_booked_cars.append(i)

    if selected_row >= len(user_booked_cars):
        show_message("Error", "Invalid selection.")
        return

    car_index = user_booked_cars[selected_row]
    car_data[car_index][1] = "Available"
    car_data[car_index][10] = ""  # Clear user ID
    save_car_data()

    # Add the returned car back to the available list
    returned_car = [
        str(car_data[car_index][0]),
        str(car_data[car_index][2]),
        str(car_data[car_index][3]),
        str(car_data[car_index][8]),
        str(car_data[car_index][7]),
        str(car_data[car_index][9]),
        str(car_data[car_index][5])
    ]
    carList.append(returned_car)

    show_message("Success", "Car successfully returned!")
    update_booking_list()
    
def load_account_info():
    account_info_label.setText(f"First Name: {userData[1].capitalize()}\nLast Name: {userData[2].capitalize()}\nEmail: {userData[3]}")

def change_email():
    new_email, ok = QInputDialog.getText(main_window, "Change Email", "Enter new email:")
    if ok and new_email:
        if any(new_email.lower() == user_data[i, 3] for i in range(len(user_data))):
            show_message("Error", "Email already in use.")
            return
        for i in range(len(user_data)):
            if user_data[i, 0] == userData[0]:
                user_data[i, 3] = new_email.lower()
                userData[3] = new_email.lower()
                save_user_data()
                show_message("Success", "Email updated successfully.")
                load_account_info()
                return

def change_password():
    new_password, ok = QInputDialog.getText(main_window, "Change Password", "Enter new password:")
    if ok and new_password:
        if (len(new_password) < 8 or not re.search(r"[A-Z]", new_password) or not re.search(r"[a-z]", new_password) or
            not re.search(r"\d", new_password) or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", new_password)):
            show_message("Weak Password", "Password must include: 8 characters, upper and lower case, a digit, and a special character.")
            return
        for i in range(len(user_data)):
            if user_data[i, 0] == userData[0]:
                user_data[i, 4] = new_password
                userData[4] = new_password
                save_user_data()
                show_message("Success", "Password updated successfully.")
                return

def delete_account():
    # Check if the user has any rented cars
    for car in car_data:
        if car[1].lower() == "unavailable" and car[10] == userData[0]:
            show_message("Error", "You must return all your cars before deleting your account.")
            return

    confirm = QMessageBox.question(main_window, "Confirm Deletion", "Are you sure you want to delete your account?",
                                   QMessageBox.Yes | QMessageBox.No)
    if confirm == QMessageBox.Yes:
        for i in range(len(user_data)):
            if user_data[i, 0] == userData[0]:
                user_data[i, 1] = "DELETED"
                user_data[i, 2] = "USER"
                user_data[i, 3] = f"deleted{user_data[i,0]}@user.com"
                user_data[i, 4] = "DELETED"
                save_user_data()
                show_message("Account Deleted", "Your account has been deleted and cannot be used again.")
                app.quit()
                return

# Event Logic
def handle_login():
    global userData
    email = email_input.text().lower()
    password = password_input.text()
    for i in range(len(user_data)):
        if email == user_data[i, 3] and password == user_data[i, 4]:
            userData = user_data[i]
            show_message("Success", "Login successful!")
            main_layout.setCurrentWidget(dashboard_widget)
            return
    show_message("Error", "Invalid email or password.")

def handle_register():
    global user_data
    fname = fname_input.text().strip().lower()
    lname = lname_input.text().strip().lower()
    email = reg_email_input.text().strip().lower()
    password = reg_password_input.text()
    confirm_password = confirm_password_input.text()

    if not re.match(r"^[a-zA-Z\s\-]+$", fname):
        show_message("Invalid Input", "First name must contain only letters, spaces, or hyphens.")
        return
    if not re.match(r"^[a-zA-Z\s\-]+$", lname):
        show_message("Invalid Input", "Last name must contain only letters, spaces, or hyphens.")
        return
    if not re.fullmatch(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", email):
        show_message("Invalid Input", "Invalid email format.")
        return
    if any(email == user_data[i, 3] for i in range(len(user_data))):
        show_message("Duplicate Email", "Email already in use.")
        return
    if password != confirm_password:
        show_message("Password Error", "Passwords do not match.")
        return
    if (len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or
        not re.search(r"\d", password) or not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        show_message("Weak Password", "Password must include: 8 characters, upper and lower case, a digit, and a special character.")
        return

    new_id = str(int(user_data[-1, 0]) + 1).zfill(4)
    new_user = [new_id, fname, lname, email, password, "False"]
    user_data = np.append(user_data, [new_user], axis=0)
    save_user_data()
    show_message("Success", "Account created.")
    main_layout.setCurrentWidget(menu_widget)

# Connections
login_button.clicked.connect(lambda: main_layout.setCurrentWidget(login_widget))
register_button.clicked.connect(lambda: main_layout.setCurrentWidget(register_widget))
login_submit.clicked.connect(handle_login)
register_submit.clicked.connect(handle_register)
option1.clicked.connect(lambda: [update_car_list(), main_layout.setCurrentWidget(car_widget)])
option2.clicked.connect(lambda: [update_booking_list(), main_layout.setCurrentWidget(booking_widget)])
option3.clicked.connect(lambda: [load_account_info(), main_layout.setCurrentWidget(account_widget)])
option4.clicked.connect(app.quit)
prev_button.clicked.connect(prev_page)
next_button.clicked.connect(next_page)
back_button.clicked.connect(lambda: main_layout.setCurrentWidget(dashboard_widget))
car_list_display.itemClicked.connect(lambda item: view_car_detail(car_list_display.currentRow()))
rent_button.clicked.connect(rent_selected_car)
back_to_list_button.clicked.connect(lambda: main_layout.setCurrentWidget(car_widget))
return_button.clicked.connect(return_selected_car)
back_to_dashboard_button.clicked.connect(lambda: main_layout.setCurrentWidget(dashboard_widget))
change_email_button.clicked.connect(change_email)
change_password_button.clicked.connect(change_password)
delete_account_button.clicked.connect(delete_account)
account_back_button.clicked.connect(lambda: main_layout.setCurrentWidget(dashboard_widget))

main_window.setWindowTitle("Car Rental Login System")
main_window.show()
sys.exit(app.exec_())
