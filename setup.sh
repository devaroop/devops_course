#!/bin/bash

# Health API Service Setup Script
# This script sets up the development environment for the Health API Service

echo "🏥 Health API Service Setup"
echo "============================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "To start the API service:"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "To run tests:"
echo "  source venv/bin/activate"
echo "  pytest"
echo ""
echo "To run the demo:"
echo "  source venv/bin/activate"
echo "  python demo.py"
echo ""
echo "API will be available at: http://localhost:8000"
echo "Documentation: http://localhost:8000/docs"
