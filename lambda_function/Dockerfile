# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY clean-energy.py .

# Expose the port (optional, for HTTP servers)
EXPOSE 8080

# Run the application
CMD ["python", "clean-energy.py"]