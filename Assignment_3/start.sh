#!/bin/bash

# Stop any process using backend or frontend ports
echo "Killing any process on ports 5000 and 3000..."
fuser -k 5000/tcp 2>/dev/null
fuser -k 3000/tcp 2>/dev/null

# Start backend
cd backend
echo "Starting Flask backend..."
export FLASK_APP=src/main.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000 &
BACKEND_PID=$!

# Start frontend
cd ../frontend
echo "Starting React frontend..."
npm start &
FRONTEND_PID=$!

# Trap Ctrl+C and kill both
trap "echo 'Stopping...'; kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT

# Wait for both to exit
wait $BACKEND_PID $FRONTEND_PID