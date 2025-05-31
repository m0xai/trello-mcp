#!/bin/bash
set -e

# Ensure required directories exist and have correct permissions
mkdir -p /app/logs
chown -R appuser:appgroup /app

# Activate virtual environment if needed
if [ -d "/app/.venv" ]; then
    source /app/.venv/bin/activate
fi

# Function to handle graceful shutdown
cleanup() {
    echo "Received shutdown signal, cleaning up..."
    # Add any cleanup tasks here
    exit 0
}

# Trap SIGTERM and SIGINT
trap cleanup SIGTERM SIGINT

# Start the application
echo "Starting Trello MCP Server..."
exec python main.py 