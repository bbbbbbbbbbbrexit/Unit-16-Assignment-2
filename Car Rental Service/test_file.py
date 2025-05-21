import numpy as np

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

for row in carList:
    print(f"{row[1]} {row[2]}")
    print(f"{row[3]} | {row[4]} | {row[5]} Seats | {row[6]} per day\n")

