import os
import logging
from typing import List
from collections.abc import AsyncIterator
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP, Context
from trello_api import TrelloClient
from trello_service import TrelloService
from models import TrelloBoard, TrelloList, TrelloCard

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create an MCP server with a descriptive name
mcp = FastMCP("Trello MCP Server")

# Load environment variables
load_dotenv()

# Initialize Trello client and service
try:
    client = TrelloClient(
        api_key=os.getenv("TRELLO_API_KEY"), token=os.getenv("TRELLO_TOKEN")
    )
    service = TrelloService(client)
    logger.info("Trello client and service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Trello client: {str(e)}")
    raise

@mcp.tool()
async def get_board(board_id: str) -> TrelloBoard:
    try:
        board = await service.get_board(board_id)
        return board
    except Exception as e:
        return str(e)


@mcp.tool()
async def get_boards() -> List[TrelloBoard]:
    return await service.get_boards()


@mcp.tool()
async def get_lists(board_id: str) -> List[TrelloList]:
    return await service.get_lists(board_id)
