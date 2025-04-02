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


# Board Tools
@mcp.tool()
async def get_board(ctx: Context, board_id: str) -> TrelloBoard:
    """Retrieves a specific board by its ID.

    Args:
        board_id (str): The ID of the board to retrieve.

    Returns:
        TrelloBoard: The board object containing board details.
    """
    try:
        logger.info(f"Getting board with ID: {board_id}")
        result = await service.get_board(board_id)
        logger.info(f"Successfully retrieved board: {board_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get board: {str(e)}"
        logger.error(error_msg)
        ctx.error(error_msg)
        raise


@mcp.tool()
async def get_boards(ctx: Context) -> List[TrelloBoard]:
    """Retrieves all boards for the authenticated user.

    Returns:
        List[TrelloBoard]: A list of board objects.
    """
    try:
        logger.info("Getting all boards")
        result = await service.get_boards()
        logger.info(f"Successfully retrieved {len(result)} boards")
        return result
    except Exception as e:
        error_msg = f"Failed to get boards: {str(e)}"
        logger.error(error_msg)
        ctx.error(error_msg)
        raise



@mcp.tool()
async def get_lists(board_id: str) -> List[TrelloList]:
    return await service.get_lists(board_id)
