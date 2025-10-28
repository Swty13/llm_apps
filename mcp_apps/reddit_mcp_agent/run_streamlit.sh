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

# Run Streamlit app
echo "🚀 Starting Reddit MCP Streamlit App..."
echo "📱 Open http://localhost:8501 in your browser"
streamlit run streamlit_app.py