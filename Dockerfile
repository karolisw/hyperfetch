# build stage
FROM node:18 as build-stage

# Set the working directory to /frontend
WORKDIR /frontend

COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the current directory contents into the container at /frontend
COPY . .

# Build the app
RUN npm run build

# Expose port 3000 to the outside world
EXPOSE 80

# URL to the backend 
ENV BACKEND="hyperfetch-backend.azurewebsites.net/api/"

# Start the app
CMD ["npm", "start"]