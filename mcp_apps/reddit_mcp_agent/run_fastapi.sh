#!/bin/bash

# Navigate to the src directory
cd "$(dirname "$0")/src"

# Source environment variables
if [ -f ".env" ]; then
    source .env
fi

# Install requirements if needed
if [ ! -f "installed.flag" ]; then
    echo "Installing requirements..."
    pip install streamlit plotly pandas praw mcp fastapi uvicorn
    touch installed.flag
fi

# Run FastAPI server
echo "🚀 Starting Reddit MCP FastAPI Server..."
echo "📖 API Documentation: http://localhost:8000/docs"
echo "🔗 Interactive API: http://localhost:8000/redoc"
python fastapi_server.py