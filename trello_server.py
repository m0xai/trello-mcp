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


# List Tools
@mcp.tool()
async def get_list(ctx: Context, list_id: str) -> TrelloList:
    """Retrieves a specific list by its ID.

    Args:
        list_id (str): The ID of the list to retrieve.

    Returns:
        TrelloList: The list object containing list details.
    """
    try:
        logger.info(f"Getting list with ID: {list_id}")
        result = await service.get_list(list_id)
        logger.info(f"Successfully retrieved list: {list_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get list: {str(e)}"
        logger.error(error_msg)
        ctx.error(error_msg)
        raise


@mcp.tool()
async def get_lists(ctx: Context, board_id: str) -> List[TrelloList]:
    """Retrieves all lists on a given board.

    Args:
        board_id (str): The ID of the board whose lists to retrieve.

    Returns:
        List[TrelloList]: A list of list objects.
    """
    try:
        logger.info(f"Getting lists for board: {board_id}")
        result = await service.get_lists(board_id)
        logger.info(f"Successfully retrieved {len(result)} lists for board: {board_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get lists: {str(e)}"
        logger.error(error_msg)
        ctx.error(error_msg)
        raise


@mcp.tool()
async def update_list(ctx: Context, list_id: str, name: str) -> TrelloList:
    """Updates the name of a list.

    Args:
        list_id (str): The ID of the list to update.
        name (str): The new name for the list.

    Returns:
        TrelloList: The updated list object.
    """
    try:
        logger.info(f"Updating list {list_id} with new name: {name}")
        result = await service.update_list(list_id, name)
        logger.info(f"Successfully updated list: {list_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to update list: {str(e)}"
        logger.error(error_msg)
        ctx.error(error_msg)
        raise


@mcp.tool()
async def delete_list(ctx: Context, list_id: str) -> TrelloList:
    """Archives a list.

    Args:
        list_id (str): The ID of the list to close.

    Returns:
        TrelloList: The archived list object.
    """
    try:
        logger.info(f"Archiving list: {list_id}")
        result = await service.delete_list(list_id)
        logger.info(f"Successfully archived list: {list_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to delete list: {str(e)}"
        logger.error(error_msg)
        ctx.error(error_msg)
        raise

