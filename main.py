import os
import logging
import asyncio
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from trello_server import mcp

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


async def start_server():
    try:
        # Verify environment variables
        if not os.getenv("TRELLO_API_KEY") or not os.getenv("TRELLO_TOKEN"):
            raise ValueError(
                "TRELLO_API_KEY and TRELLO_TOKEN must be set in environment variables"
            )

        logger.info("Starting Trello MCP Server...")
        await mcp.start()
        logger.info("Trello MCP Server started successfully")

        # Keep the server running
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        raise


def main():
    try:
        asyncio.run(start_server())
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
