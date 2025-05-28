FROM python:3.12-slim

WORKDIR /app

# Install only necessary system dependencies for build, then remove them
COPY pyproject.toml uv.lock ./
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    pip install --no-cache-dir uv && \
    uv pip install --system -e . && \
    pip install --no-cache-dir fastmcp==2.5.1 && \
    apt-get purge -y --auto-remove build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Create non-root user and set ownership
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

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