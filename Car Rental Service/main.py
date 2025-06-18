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
    
def clear_login_fields():
    email_input.clear()
    password_input.clear()

def clear_register_fields():
    fname_input.clear()
    lname_input.clear()
    reg_email_input.clear()
    reg_password_input.clear()
    confirm_password_input.clear()


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
# Manage Users Widget
# ===============================

manage_users_widget = QWidget()
manage_users_layout = QVBoxLayout(manage_users_widget)

user_list_display = QListWidget()
manage_user_action_button = QPushButton("Manage Selected User")
back_from_users = QPushButton("Back to Dashboard")

manage_users_layout.addWidget(user_list_display)
manage_users_layout.addWidget(manage_user_action_button)
manage_users_layout.addWidget(back_from_users)



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
            car[1] = "available"
            car[10] = ""
            break

    save_car_data()
    update_booking_list()
    update_car_list()
    show_message("Success", "Car returned.")
    
def assign_selected_car_to_user():
    selected = car_list_display.currentRow()
    if selected == -1:
        show_message("Error", "Select a car first.")
        return

    available_cars = [car for car in car_data if car[1].lower() == "available"]
    if selected >= len(available_cars):
        show_message("Error", "Invalid selection.")
        return

    car_id = available_cars[selected][0]
    car_idx = next((i for i, c in enumerate(car_data) if c[0] == car_id), None)

    eligible_users = [f"{u[0]} - {u[3]}" for u in user_data if u[5].strip().lower() != "true"]
    if not eligible_users:
        show_message("Error", "No non-admin users available.")
        return

    selected_user, ok = QInputDialog.getItem(main_window, "Assign to User", "Select a user:", eligible_users, 0, False)
    if ok:
        user_id = selected_user.split(":")[0].strip()
        car_data[car_idx][1] = "Unavailable"
        car_data[car_idx][10] = user_id
        save_car_data()
        update_car_list()
        show_message("Success", f"Car {car_id} assigned to user {user_id}.")
   
def return_selected_car():
    selected = car_list_display.currentRow()
    if selected == -1:
        show_message("Error", "Select a car first.")
        return
    
    # Show only cars that are unavailable
    unavailable_cars = [car for car in car_data if car[1].lower() == "unavailable"]
    if selected >= len(unavailable_cars):
        show_message("Error", "Invalid selection.")
        return

    car_id = unavailable_cars[selected][0]
    car_idx = next((i for i, c in enumerate(car_data) if c[0] == car_id), None)

    if car_idx is not None:
        car_data[car_idx][1] = "available"
        car_data[car_idx][10] = ""  # clear assigned user
        save_car_data()
        update_car_list()
        show_message("Success", f"Car {car_id} returned and marked available.")

def change_email_address():
    if userData[0] == "0000":
        show_message("Blocked", "The debug account cannot change its email.")
        return

    new_email, ok = QInputDialog.getText(main_window, "Change Email", "Enter new email:")
    if ok and new_email:
        for i in range(len(user_data)):
            if user_data[i][0] == userData[0]:
                user_data[i][3] = new_email
                userData[3] = new_email  # sync session
                save_user_data()
                load_account_info()
                show_message("Success", "Email updated.")
                return

def change_password():
    if userData[0] == "0000":
        show_message("Blocked", "The debug account cannot change its password.")
        return

    current_password, ok1 = QInputDialog.getText(main_window, "Verify Password", "Enter current password:")
    if not ok1 or current_password != userData[4]:
        show_message("Error", "Password incorrect or cancelled.")
        return

    new_password, ok2 = QInputDialog.getText(main_window, "New Password", "Enter new password:")
    if ok2 and new_password:
        for i in range(len(user_data)):
            if user_data[i][0] == userData[0]:
                user_data[i][4] = new_password
                userData[4] = new_password  # sync session
                save_user_data()
                show_message("Success", "Password updated.")
                return

def delete_account_confirm():
    global user_data, userData

    if userData[0] == "0000":
        show_message("Blocked", "The debug account cannot be deleted.")
        return

    # Check for unreturned cars
    has_rented_cars = any(car[10] == userData[0] and car[1].lower() == "unavailable" for car in car_data)
    if has_rented_cars:
        show_message("Blocked", "Return all rented cars before deleting your account.")
        return

    # Confirm delete
    confirm, ok = QInputDialog.getText(main_window, "Delete Account", "Type DELETE to confirm:")
    if not (ok and confirm.strip().upper() == "DELETE"):
        show_message("Cancelled", "Account deletion cancelled.")
        return

    # Soft-delete: mark first and last name
    for i in range(len(user_data)):
        if user_data[i][0] == userData[0]:
            user_data[i][5] = "deleted"  # Mark as deleted (custom flag)
            break

    save_user_data()
    userData = None
    show_message("Account Deleted", "Your account has been marked as deleted.")
    main_layout.setCurrentWidget(menu_widget)

def update_user_list():
    user_list_display.clear()
    for user in user_data:
        status = user[5].strip().capitalize()
        name_display = f"{user[1]} {user[2]}" if status != "Deleted" else "(Deleted User)"
        user_list_display.addItem(f"{user[0]} - {name_display} | Status: {status}")

def manage_selected_user():
    selected = user_list_display.currentRow()
    if selected == -1:
        show_message("Error", "Select a user first.")
        return

    user_entry = user_list_display.item(selected).text()
    user_id = user_entry.split(" - ")[0].strip()

    if user_id == "0000":
        show_message("Blocked", "You cannot modify the debug account.")
        return

    if user_id == userData[0]:
        show_message("Blocked", "You cannot modify your own account from the admin panel.")
        return

    idx = next((i for i, u in enumerate(user_data) if u[0] == user_id), None)

    if idx is None:
        show_message("Error", "User not found.")
        return

    is_deleted = user_data[idx][5].strip().lower() == "deleted"

    if is_deleted:
        options = ["Restore Account"]
    else:
        options = ["Return All Cars", "Toggle Admin", "Delete Account"]

    choice, ok = QInputDialog.getItem(main_window, "Manage User", "Choose an action:", options, 0, False)
    if not ok:
        return

    if choice == "Return All Cars":
        for car in car_data:
            if car[10] == user_id and car[1].lower() == "unavailable":
                car[1] = "available"
                car[10] = ""
        save_car_data()
        show_message("Success", "All cars returned for user.")

    elif choice == "Toggle Admin":
        current = user_data[idx][5].strip().lower()
        user_data[idx][5] = "false" if current == "true" else "True"
        save_user_data()
        show_message("Success", "Admin status updated.")

    elif choice == "Delete Account":
        has_rented = any(car[10] == user_id and car[1].lower() == "unavailable" for car in car_data)
        if has_rented:
            show_message("Blocked", "User must return all cars before deletion.")
            return
        user_data[idx][5] = "deleted"
        save_user_data()
        show_message("Success", "Account marked as deleted.")

    elif choice == "Restore Account":
        user_data[idx][5] = "false"  # Restored users default to non-admin
        save_user_data()
        show_message("Success", "Account restored.")

    update_user_list()

def load_account_info():
    account_info.setText(f"Name: {userData[1].capitalize()} {userData[2].capitalize()}\nEmail: {userData[3]}")

def handle_login():
    global userData
    email = email_input.text().lower()
    password = password_input.text()
    for user in user_data:
        if email == user[3] and password == user[4]:
            if user[5].strip().lower() == "deleted":
                show_message("Error", "This account has been deleted and cannot be used.")
                clear_login_fields()
                return
            userData = user
            update_dashboard()
            update_car_list()
            main_layout.setCurrentWidget(dashboard_widget)
            clear_login_fields()
            return
    show_message("Error", "Invalid login credentials.")
    clear_login_fields()


def handle_register():
    global user_data

    fname = fname_input.text().strip().lower()
    lname = lname_input.text().strip().lower()
    email = reg_email_input.text().strip().lower()
    password = reg_password_input.text()
    confirm_password = confirm_password_input.text()

    # === Name validation
    if not re.match(r"^[a-zA-Z\s\-]+$", fname):
        show_message("Invalid Input", "First name must contain only letters, spaces, or hyphens.")
        return
    if not re.match(r"^[a-zA-Z\s\-]+$", lname):
        show_message("Invalid Input", "Last name must contain only letters, spaces, or hyphens.")
        return

    # === Email format
    if not re.fullmatch(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", email):
        show_message("Invalid Input", "Invalid email format.")
        return

    # === Duplicate email check
    if any(email == user_data[i, 3] for i in range(len(user_data))):
        show_message("Duplicate Email", "Email already in use.")
        return

    # === Password checks
    if password != confirm_password:
        show_message("Password Error", "Passwords do not match.")
        return

    if (len(password) < 8 or
        not re.search(r"[A-Z]", password) or
        not re.search(r"[a-z]", password) or
        not re.search(r"\d", password) or
        not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        show_message("Weak Password", "Password must include at least 8 characters, an uppercase letter, a lowercase letter, a digit, and a special character.")
        return

    # === New ID generation
    new_id = str(int(user_data[-1, 0]) + 1).zfill(4) if len(user_data) else "0001"
    new_user = [new_id, fname, lname, email, password, "False"]
    user_data = np.append(user_data, [new_user], axis=0)

    save_user_data()
    show_message("Success", "Account created.")
    clear_register_fields()
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
login_button.clicked.connect(lambda: [clear_login_fields(), main_layout.setCurrentWidget(login_widget)])
register_button.clicked.connect(lambda: [clear_register_fields(), main_layout.setCurrentWidget(register_widget)])
login_submit.clicked.connect(handle_login)
email_input.returnPressed.connect(handle_login)
password_input.returnPressed.connect(handle_login)
register_submit.clicked.connect(handle_register)
option1.clicked.connect(lambda: [update_car_list(), update_car_buttons(), main_layout.setCurrentWidget(car_widget)])
option2_user.clicked.connect(lambda: [update_booking_list(), main_layout.setCurrentWidget(booking_widget)])
option2_admin.clicked.connect(lambda: [update_user_list(), main_layout.setCurrentWidget(manage_users_widget)])
option3.clicked.connect(lambda: [load_account_info(), main_layout.setCurrentWidget(account_widget)])
option4.clicked.connect(lambda: main_layout.setCurrentWidget(menu_widget))
debugSpecial.clicked.connect(toggle_debug_admin)
rent_button.clicked.connect(rent_selected_car)
admin_book_button.clicked.connect(assign_selected_car_to_user)
admin_return_button.clicked.connect(return_selected_car)
change_email.clicked.connect(change_email_address)
change_pass.clicked.connect(change_password)
delete_account.clicked.connect(delete_account_confirm)
back_to_dashboard.clicked.connect(lambda: main_layout.setCurrentWidget(dashboard_widget))
back_from_users.clicked.connect(lambda: main_layout.setCurrentWidget(dashboard_widget))
manage_user_action_button.clicked.connect(manage_selected_user)
return_button.clicked.connect(return_selected_car)
booking_back.clicked.connect(lambda: main_layout.setCurrentWidget(dashboard_widget))
account_back.clicked.connect(lambda: main_layout.setCurrentWidget(dashboard_widget))


# ===============================
# Add and Show
# ===============================
for w in [menu_widget, login_widget, register_widget, dashboard_widget,
          car_widget, booking_widget, account_widget, manage_users_widget]:
    main_layout.addWidget(w)

main_window.setWindowTitle("Car Rental System")
main_layout.setCurrentWidget(menu_widget)
main_window.show()
sys.exit(app.exec_())
