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
async def create_list(
    ctx: Context, board_id: str, name: str, pos: str = "bottom"
) -> TrelloList:
    """Creates a new list on a given board.

    Args:
        board_id (str): The ID of the board to create the list in.
        name (str): The name of the new list.
        pos (str, optional): The position of the new list. Can be "top" or "bottom". Defaults to "bottom".

    Returns:
        TrelloList: The newly created list object.
    """
    try:
        logger.info(f"Creating list '{name}' in board: {board_id}")
        result = await service.create_list(board_id, name, pos)
        logger.info(f"Successfully created list '{name}' in board: {board_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to create list: {str(e)}"
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


# Card Tools
@mcp.tool()
async def get_card(ctx: Context, card_id: str) -> TrelloCard:
    """Retrieves a specific card by its ID.

    Args:
        card_id (str): The ID of the card to retrieve.

    Returns:
        TrelloCard: The card object containing card details.
    """
    try:
        logger.info(f"Getting card with ID: {card_id}")
        result = await service.get_card(card_id)
        logger.info(f"Successfully retrieved card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get card: {str(e)}"
        logger.error(error_msg)
        ctx.error(error_msg)
        raise


@mcp.tool()
async def get_cards(ctx: Context, list_id: str) -> List[TrelloCard]:
    """Retrieves all cards in a given list.

    Args:
        list_id (str): The ID of the list whose cards to retrieve.

    Returns:
        List[TrelloCard]: A list of card objects.
    """
    try:
        logger.info(f"Getting cards for list: {list_id}")
        result = await service.get_cards(list_id)
        logger.info(f"Successfully retrieved {len(result)} cards for list: {list_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to get cards: {str(e)}"
        logger.error(error_msg)
        ctx.error(error_msg)
        raise


@mcp.tool()
async def create_card(
    ctx: Context, list_id: str, name: str, desc: str = None
) -> TrelloCard:
    """Creates a new card in a given list.

    Args:
        list_id (str): The ID of the list to create the card in.
        name (str): The name of the new card.
        desc (str, optional): The description of the new card. Defaults to None.

    Returns:
        TrelloCard: The newly created card object.
    """
    try:
        logger.info(f"Creating card in list {list_id} with name: {name}")
        result = await service.create_card(list_id, name, desc)
        logger.info(f"Successfully created card in list: {list_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to create card: {str(e)}"
        logger.error(error_msg)
        ctx.error(error_msg)
        raise


@mcp.tool()
async def update_card(ctx: Context, card_id: str, **kwargs) -> TrelloCard:
    """Updates a card's attributes.

    Args:
        card_id (str): The ID of the card to update.
        **kwargs: Keyword arguments representing the attributes to update on the card.

    Returns:
        TrelloCard: The updated card object.
    """
    try:
        logger.info(f"Updating card {card_id} with attributes: {kwargs}")
        result = await service.update_card(card_id, **kwargs)
        logger.info(f"Successfully updated card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to update card: {str(e)}"
        logger.error(error_msg)
        ctx.error(error_msg)
        raise


@mcp.tool()
async def delete_card(ctx: Context, card_id: str) -> dict:
    """Deletes a card.

    Args:
        card_id (str): The ID of the card to delete.

    Returns:
        dict: The response from the delete operation.
    """
    try:
        logger.info(f"Deleting card: {card_id}")
        result = await service.delete_card(card_id)
        logger.info(f"Successfully deleted card: {card_id}")
        return result
    except Exception as e:
        error_msg = f"Failed to delete card: {str(e)}"
        logger.error(error_msg)
        ctx.error(error_msg)
        raise


# Add a prompt for common Trello operations
@mcp.prompt()
def trello_help() -> str:
    """Provides help information about available Trello operations."""
    return """
    Available Trello Operations:
    1. Board Operations:
       - Get a specific board
       - List all boards
    2. List Operations:
       - Get a specific list
       - List all lists in a board
       - Create a new list
       - Update a list's name
       - Archive a list
    3. Card Operations:
       - Get a specific card
       - List all cards in a list
       - Create a new card
       - Update a card's attributes
       - Delete a card
    """
