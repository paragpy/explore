#!/bin/bash

echo "======================================"
echo "Graph Database API - Quick Start"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Step 1: Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Step 2: Running migrations..."
python manage.py migrate

echo ""
echo "Step 3: Starting development server..."
echo ""
echo "======================================"
echo "Server will start at: http://127.0.0.1:8000/"
echo "Swagger UI: http://127.0.0.1:8000/swagger/"
echo "ReDoc: http://127.0.0.1:8000/redoc/"
echo "======================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver
