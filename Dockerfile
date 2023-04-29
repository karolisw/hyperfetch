# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /backend

# Copy the current directory contents into the container at /app
COPY ./src /backend/src
COPY main.py /backend
COPY requirements.txt /backend
COPY .gitignore /backend/.gitignore
COPY LICENSE /backend

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV MONGODB_URL="mongodb+srv://admin:adminKaroline12@hyperfetch.qwivycp.mongodb.net/test"
ENV MONGO_DB="hyperfetch"
ENV MONGO_COLLECTION="runs"

# Run the command to start the server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
