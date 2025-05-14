FROM python:3.12-slim

# Add metadata labels
LABEL description="Trello MCP Server"
LABEL version="1.0"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1000 appuser

# Install Python dependencies
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && \
    uv pip install --system -e .

# Copy application code
COPY . .

# Set ownership to non-root user
RUN chown -R appuser:appuser /app

# Set default environment variables
ENV PYTHONUNBUFFERED=1
ENV USE_CLAUDE_APP=false
ENV MCP_SERVER_NAME="Trello MCP Server"
ENV MCP_SERVER_HOST=0.0.0.0
ENV MCP_SERVER_PORT=8952

# Expose port
EXPOSE ${MCP_SERVER_PORT}

# Switch to non-root user
USER appuser

# Run the application
CMD ["python", "main.py"] 