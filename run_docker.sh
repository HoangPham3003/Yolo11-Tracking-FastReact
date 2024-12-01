#!/bin/bash

# Wait for ngrok-frontend to be ready
echo "Waiting for ngrok-frontend to be ready..."
until curl -s http://localhost:4040/api/tunnels > /dev/null; do
  echo "Waiting for ngrok-frontend service to start..."
  sleep 2
done

# Fetch the ngrok-frontend URL
FRONTEND_NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*' | grep -o '[^"]*$')
if [ -z "$FRONTEND_NGROK_URL" ]; then
  echo "Error: Unable to fetch ngrok-frontend URL."
  exit 1
fi
echo "Frontend ngrok URL: $FRONTEND_NGROK_URL"

# Run docker-compose with the dynamic variables
docker-compose up --build
