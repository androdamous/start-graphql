# Use the official Python 3.12 image as the base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements file to the working directory
COPY requirements.txt ./

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Run the sampling_data.py script to populate the database
RUN python sampling_data.py

# Expose the port the app runs on
EXPOSE 8000

# Define the command to run the application
CMD ["uvicorn", "telematic_products:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
