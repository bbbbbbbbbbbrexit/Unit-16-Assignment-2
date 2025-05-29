from optparse import Option
import numpy as np
from clear_console import clr

def carMenu(carList):
    rowCount = len(carList)
    menuPage = 1
    global printStart
    printAmount = 10
    while True:
        # Calculate start and end indices for the current page
        printStart = (menuPage - 1) * 10
        printEnd = min(printStart + 10, rowCount)
        printAmount = printEnd - printStart

        clr()
        for i in range(printAmount):
            row = carList[printStart + i]
            print(f"{row[1]} {row[2]}  [{printStart + i + 1}]")
            print(f"{row[3]} | {row[4]} | {row[5]} Seats | {row[6]} per day\n")
        option = input("Pick an option or N/P for the Next/Previous page: ").strip().lower()

        if option == "n":
            if printEnd >= rowCount:
                clr()
                input("You are on the last page. Press enter to continue.")
            else:
                menuPage += 1
        elif option == "p":
            if menuPage == 1:
                clr()
                input("You are on the first page. Press enter to continue.")
            else:
                menuPage -= 1
        elif option.isdigit():
            return option
        else:
            input("Invalid option. Press enter to continue.\n")

global filePath
global car_data
global car_info_data

filePath = "Car Rental Service/car_data.csv"
car_data = np.loadtxt(filePath, delimiter=",", dtype=str, skiprows=1)

carList = []

for i in range(len(car_data)):
    if car_data[i][1].lower() == "unavailable":
            continue

    carEntry = [str(car_data[i][0]), str(car_data[i][2]), str(car_data[i][3]), str(car_data[i][8]), str(car_data[i][7]), str(car_data[i][9]), str(car_data[i][5])]
    carList.append(carEntry)
    
carMenu(carList)