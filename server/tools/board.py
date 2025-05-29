"""
This module contains tools for managing Trello boards.
"""

import logging
from typing import List

from mcp.server.fastmcp import Context
from fastmcp import FastMCP

from server.models import TrelloBoard
from server.services.board import BoardService
from server.trello import client
from server.mcp_instance import mcp

logger = logging.getLogger(__name__)

service = BoardService(client)


@mcp.tool()
async def get_board(context: Context, board_id: str) -> TrelloBoard:
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
        await context.error(error_msg)
        raise


@mcp.tool()
async def get_boards(context: Context) -> List[TrelloBoard]:
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
        await context.error(error_msg)
        raise
