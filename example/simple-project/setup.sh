#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}FastAPI Dapr Example - Setup Script${NC}"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3.11+"
    exit 1
fi

# Create virtual environment
echo -e "${BLUE}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "1. To run with Docker Compose:"
echo "   docker-compose up --build"
echo ""
echo "2. Or to run locally with Dapr:"
echo "   source venv/bin/activate"
echo "   dapr run --app-id fastapi-service --app-port 8000 -- python main.py"
echo ""
echo "3. View API docs at: http://localhost:8000/docs"
