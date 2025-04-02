import os
from typing import List
from dotenv import load_dotenv
from mcp.server import FastMCP
from trello_api import TrelloClient
from trello_service import TrelloService, TrelloBoard, TrelloList


mcp = FastMCP("Trello MCP Server")

load_dotenv()
client = TrelloClient(
    api_key=os.getenv("TRELLO_API_KEY"), token=os.getenv("TRELLO_TOKEN")
)
service = TrelloService(client)


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
