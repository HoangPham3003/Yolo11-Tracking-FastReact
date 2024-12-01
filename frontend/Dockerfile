# Use Node.js to build the frontend
FROM node:16 as build

# Set the working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the application for production
RUN npm run build

# Expose the port that Nginx will serve on
EXPOSE 3000

# Start Nginx
CMD ["npm", "start"]