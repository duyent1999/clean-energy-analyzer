# Use an official Python runtime as a parent image
FROM public.ecr.aws/lambda/python:3.9

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY clean-energy.py .

# Run the application
CMD ["clean-energy.lambda_handler"]