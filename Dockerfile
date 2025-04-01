# Use the official Python image as the base image
FROM python:3.10-slim

# Install wget
RUN apt-get update && apt-get install -y wget

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["python", "bot.py"]
