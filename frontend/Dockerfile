# frontend/Dockerfile

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

# Use an nginx image to serve the frontend
FROM nginx:alpine

# Copy the build output to nginx’s default html location
COPY --from=build /app/build /usr/share/nginx/html

# Expose the port that Nginx will serve on
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]