import numpy as np

# Step 1: Create car data as a 2D list
car_data = [
    ["carID", "carStatus", "carRates"],  # Header
    ["0001", "available", "20"],
    ["0002", "unavailable", "25"],
    ["0003", "available", "30"]
]

# Step 2: Convert to NumPy array (optional, but useful for saving)
data_array = np.array(car_data)

# Step 3: Define file path
text_file_path = 'car_data.csv'

# Step 4: Save the array to a CSV-formatted text file
# Using fmt='%s' to treat all values as strings
np.savetxt(text_file_path, data_array, fmt='%s', delimiter=',')

# Step 5 (Optional): Read it back and print
loaded_array = np.loadtxt(text_file_path, delimiter=',', dtype=str)

print("Loaded Data from File:")
print(loaded_array)