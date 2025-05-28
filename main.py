import logging
import os
from typing import Optional

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Import all tools
from server.tools.board import get_board as _get_board, get_boards as _get_boards
from server.tools.card import get_card as _get_card, get_cards as _get_cards
from server.tools.checklist import (
    get_checklist as _get_checklist,
    get_card_checklists as _get_card_checklists,
    create_checklist as _create_checklist,
    update_checklist as _update_checklist,
    delete_checklist as _delete_checklist,
    add_checkitem as _add_checkitem,
    update_checkitem as _update_checkitem,
    delete_checkitem as _delete_checkitem,
)
from server.tools.list import get_list as _get_list, get_lists as _get_lists, create_list as _create_list, update_list as _update_list, delete_list as _delete_list

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize MCP server with tools
mcp = FastMCP("Trello MCP Server")

# Register tools
@mcp.tool()
async def get_board(context, board_id: str):
    return await _get_board(context, board_id)

@mcp.tool()
async def get_boards(context):
    return await _get_boards(context)

@mcp.tool()
async def get_card(context, card_id: str):
    return await _get_card(context, card_id)

@mcp.tool()
async def get_cards(context, list_id: str, from_date: Optional[str] = None):
    return await _get_cards(context, list_id, from_date)

@mcp.tool()
async def get_checklist(context, checklist_id: str):
    return await _get_checklist(context, checklist_id)

@mcp.tool()
async def get_card_checklists(context, card_id: str):
    return await _get_card_checklists(context, card_id)

@mcp.tool()
async def create_checklist(context, card_id: str, name: str, pos: Optional[str] = None):
    return await _create_checklist(context, card_id, name, pos)

@mcp.tool()
async def update_checklist(context, checklist_id: str, name: Optional[str] = None, pos: Optional[str] = None):
    return await _update_checklist(context, checklist_id, name, pos)

@mcp.tool()
async def delete_checklist(context, checklist_id: str):
    return await _delete_checklist(context, checklist_id)

@mcp.tool()
async def add_checkitem(context, checklist_id: str, name: str, checked: bool = False, pos: Optional[str] = None):
    return await _add_checkitem(context, checklist_id, name, checked, pos)

@mcp.tool()
async def update_checkitem(context, checklist_id: str, checkitem_id: str, name: Optional[str] = None, checked: Optional[bool] = None, pos: Optional[str] = None):
    return await _update_checkitem(context, checklist_id, checkitem_id, name, checked, pos)

@mcp.tool()
async def delete_checkitem(context, checklist_id: str, checkitem_id: str):
    return await _delete_checkitem(context, checklist_id, checkitem_id)

@mcp.tool()
async def get_list(context, list_id: str):
    return await _get_list(context, list_id)

@mcp.tool()
async def get_lists(context, board_id: str):
    return await _get_lists(context, board_id)

@mcp.tool()
async def create_list(context, board_id: str, name: str, pos: str = "bottom"):
    return await _create_list(context, board_id, name, pos)

@mcp.tool()
async def update_list(context, list_id: str, name: str):
    return await _update_list(context, list_id, name)

@mcp.tool()
async def delete_list(context, list_id: str):
    return await _delete_list(context, list_id)

if __name__ == "__main__":
    try:
        # Verify environment variables
        if not os.getenv("TRELLO_API_KEY") or not os.getenv("TRELLO_TOKEN"):
            raise ValueError(
                "TRELLO_API_KEY and TRELLO_TOKEN must be set in environment variables"
            )

        use_claude = os.getenv("USE_CLAUDE_APP", "true").lower() == "true"
        host = os.getenv("MCP_SERVER_HOST", "0.0.0.0")
        port = int(os.getenv("MCP_SERVER_PORT", "8952"))

        if use_claude:
            logger.info("Starting Trello MCP Server in Claude app mode...")
            mcp.run()  # Default: stdio transport for Claude
            logger.info("Trello MCP Server started successfully")
        else:
            logger.info(f"Starting Trello MCP Server in SSE mode at {host}:{port} ...")
            mcp.run(transport="sse")
            logger.info("Trello MCP Server started successfully")
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise
