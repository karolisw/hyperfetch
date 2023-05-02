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
COPY README.md /backend
#COPY cert.pem /backend
#COPY key.pem /backend


# Install the required packages
RUN pip install -r requirements.txt

# install the ca-certificates package
# RUN apt-get update && apt-get install -y ca-certificates
#RUN apt-get update && apt-get install -y --no-install-recommends \
 #   ca-certificates && update-ca-certificates
# update the SSL certificates
#RUN update-ca-certificates

# Make port 443 available to the world outside this container
EXPOSE 443

# Define environment variable
ENV ALLOWED_HOSTS="*" 
#"https://white-rock-097162f03.3.azurestaticapps.net",*
ENV MONGODB_URL="mongodb+srv://admin:adminKaroline12@hyperfetch.zxjvuqd.mongodb.net/?retryWrites=true&w=majority"
ENV MONGO_DB="hyperfetch"
ENV MONGO_COLLECTION="runs"
ENV PORT=443
#ENV SSL_CERT $SSL_CERT
#ENV SSL_KEY $SSL_KEY

#ENV SSL_CERTFILE="./cert.pem"
#ENV SSL_KEYFILE="./key.pem"

# Run the command to start the server
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443", "--ssl-keyfile", "${SSL_KEY}", "--ssl-certfile", "${SSL_CERT}"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "443"]
