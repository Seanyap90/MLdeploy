import csv
import random
import time

# Define the path to the CSV file
csv_file_path = 'sensor_data.csv'

# Function to generate random sensor data with different ranges
def generate_sensor_data():
    # Specify the range for each element (adjust as needed)
    range_1 = (1.82, 37.22)
    range_2 = (992.88, 1034.30)
    range_3 = (24.56, 100.0)
    range_4 = (25.35, 82.57)

    data = [
        random.uniform(range_1[0], range_1[1]),
        random.uniform(range_2[0], range_2[1]),
        random.uniform(range_3[0], range_3[1]),
        random.uniform(range_4[0], range_4[1])
    ]
    
    return data

# Function to append sensor data to the CSV file
def log_sensor_data():
    sensor_data = generate_sensor_data()
    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(sensor_data)

if __name__ == "__main__":
    # Define the interval for logging data (in seconds)
    logging_interval = 15  # Adjust as needed
    
    while True:
        log_sensor_data()
        time.sleep(logging_interval)