# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install numpy joblib scikit-learn

# Define environment variable
ENV MODEL_FILE=/app/model/ppmodel.joblib

# Run the inference script as the entry point
CMD ["python3", "inference.py"]
