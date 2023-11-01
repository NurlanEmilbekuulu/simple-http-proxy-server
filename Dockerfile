# Use an official Python runtime as a base image
FROM python:3.9-alpine

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 9097 available to the world outside this container
EXPOSE 9097

# Run app.py when the container launches
CMD ["python", "-m", "proxy_server.app"]
