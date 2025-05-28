import logging
import os
from typing import Optional

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Import all tools
from server.tools import *

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
    return await get_board(context, board_id)

@mcp.tool()
async def get_boards(context):
    return await get_boards(context)

@mcp.tool()
async def get_card(context, card_id: str):
    return await get_card(context, card_id)

@mcp.tool()
async def get_cards(context, list_id: str, from_date: Optional[str] = None):
    return await get_cards(context, list_id, from_date)

@mcp.tool()
async def get_checklist(context, checklist_id: str):
    return await get_checklist(context, checklist_id)

@mcp.tool()
async def get_card_checklists(context, card_id: str):
    return await get_card_checklists(context, card_id)

@mcp.tool()
async def create_checklist(context, card_id: str, name: str, pos: Optional[str] = None):
    return await create_checklist(context, card_id, name, pos)

@mcp.tool()
async def update_checklist(context, checklist_id: str, name: Optional[str] = None, pos: Optional[str] = None):
    return await update_checklist(context, checklist_id, name, pos)

@mcp.tool()
async def delete_checklist(context, checklist_id: str):
    return await delete_checklist(context, checklist_id)

@mcp.tool()
async def add_checkitem(context, checklist_id: str, name: str, checked: bool = False, pos: Optional[str] = None):
    return await add_checkitem(context, checklist_id, name, checked, pos)

@mcp.tool()
async def update_checkitem(context, checklist_id: str, checkitem_id: str, name: Optional[str] = None, checked: Optional[bool] = None, pos: Optional[str] = None):
    return await update_checkitem(context, checklist_id, checkitem_id, name, checked, pos)

@mcp.tool()
async def delete_checkitem(context, checklist_id: str, checkitem_id: str):
    return await delete_checkitem(context, checklist_id, checkitem_id)

@mcp.tool()
async def get_list(context, list_id: str):
    return await get_list(context, list_id)

@mcp.tool()
async def get_lists(context, board_id: str):
    return await get_lists(context, board_id)

@mcp.tool()
async def create_list(context, board_id: str, name: str, pos: str = "bottom"):
    return await create_list(context, board_id, name, pos)

@mcp.tool()
async def update_list(context, list_id: str, name: str):
    return await update_list(context, list_id, name)

@mcp.tool()
async def delete_list(context, list_id: str):
    return await delete_list(context, list_id)

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
