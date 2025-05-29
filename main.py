import logging
import os
from dotenv import load_dotenv
from server.mcp_instance import mcp
import server.tools.board
import server.tools.card
import server.tools.list
import server.tools.checklist

logger = logging.getLogger(__name__)

# Set httpx logger to ERROR to avoid leaking sensitive data
logging.getLogger("httpx").setLevel(logging.ERROR)

# Add a console handler for development
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Load environment variables
load_dotenv()

host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
port = int(os.getenv("MCP_SERVER_PORT", "8000"))
mcp.settings.host = host
mcp.settings.port = port

if __name__ == "__main__":
    try:
        # Verify environment variables
        if not os.getenv("TRELLO_API_KEY") or not os.getenv("TRELLO_TOKEN"):
            raise ValueError(
                "TRELLO_API_KEY and TRELLO_TOKEN must be set in environment variables"
            )
        use_claude = os.getenv("USE_CLAUDE_APP", "true").lower() == "true"
        if use_claude:
            logger.info("Starting Trello MCP Server in Claude app mode...")
            mcp.run(transport="stdio")  # Explicitly use stdio transport for Claude
        else:
            logger.info(f"Starting Trello MCP Server in SSE mode at http://{host}:{port}/sse")
            mcp.run(transport="sse")
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise
