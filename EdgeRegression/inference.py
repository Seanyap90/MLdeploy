import joblib
import numpy as np
import time
import csv

# Define a function to perform inference on the first element of each CSV line
def perform_inference_from_csv():
    try:
        # Load the pre-trained scikit-learn model
        model = joblib.load('/app/model/ppmodel.joblib')  # Update the path as needed

        # Read the latest line from the CSV file
        with open('/full_path_of_directory/sensor_data.csv', mode='r') as file:
            csv_reader = csv.reader(file)
            latest_row = list(csv_reader)[-1]  # Get the last row of the CSV

        # Extract the first element (assuming it's the sensor data)
        latest_sensor_data = float(latest_row[0])

        # Perform inference
        prediction = model.predict([[latest_sensor_data]])

        # Return the prediction (you can customize this)
        return prediction.tolist()
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    while True:
        # Perform inference on the first element of the latest CSV line
        result = perform_inference_from_csv()
        print("Inference result:", result)

        # Adjust the sleep interval (in seconds) as needed for your real-time requirements
        time.sleep(1)  # Sleep for 1 second between inference iterations