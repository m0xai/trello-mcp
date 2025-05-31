# Build stage
FROM python:3.12-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv and create virtual environment
RUN pip install --no-cache-dir uv && \
    python -m venv /app/.venv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN . /app/.venv/bin/activate && \
    uv pip install --system -e . && \
    pip install --no-cache-dir fastmcp==2.5.1 fastapi uvicorn

# Final stage
FROM python:3.12-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tini \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY . .

# Create non-root user and group
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --shell /bin/bash --create-home appuser && \
    chown -R appuser:appgroup /app

# Set default environment variables
ENV PYTHONUNBUFFERED=1 \
    USE_CLAUDE_APP=false \
    MCP_SERVER_NAME="Trello MCP Server" \
    MCP_SERVER_HOST=0.0.0.0 \
    MCP_SERVER_PORT=8952

# Expose port
EXPOSE ${MCP_SERVER_PORT}

# Copy and set up entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch to non-root user
USER appuser

# Use tini as init system
ENTRYPOINT ["/usr/bin/tini", "--", "/entrypoint.sh"] 