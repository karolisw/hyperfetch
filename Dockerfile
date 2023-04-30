# Use an official Node runtime as a parent image
FROM node:18

# Set the working directory to /frontend
WORKDIR /frontend

COPY package*.json ./

# Install the 'serve' package
RUN npm install -g serve

# Copy the current directory contents into the container at /frontend
COPY . .

# Install dependencies
RUN npm install


# Build the app
RUN npm run build

# Expose port 3000 to the outside world
EXPOSE 3000

# Start the app
CMD [ "npm", "run", "start" ]