# Use the official Python image as base
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY templates /app/templates
COPY statc /app/static

COPY web.py .

COPY .env .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "web.py"]
