#!/bin/bash

# AGBOT Application Startup Script

echo "🌱 Starting AGBOT Plant Health Monitoring System..."
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Navigate to app directory
cd "$(dirname "$0")"

# Install dependencies if needed
echo "📦 Checking dependencies..."
pip install -q -r requirements.txt --break-system-packages 2>/dev/null || pip install -q -r requirements.txt

# Start the Flask application
echo "🚀 Starting Flask server..."
echo ""
echo "✅ AGBOT is running!"
echo "📱 Open your browser and navigate to: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the application
python3 app.py
