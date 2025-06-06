# Use an official Python runtime as a parent image
FROM python:3.11.4-slim-bullseye

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY . /app

# Install the package and its dependencies
RUN pip install --no-cache-dir .

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run the application with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
