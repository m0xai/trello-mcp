"""
This module contains tools for managing Trello boards, lists, and cards.
"""

from server.tools import board, card, list


def register_tools(mcp):
    """Register tools with the MCP server."""
    # Board Tools
    mcp.add_tool(board.get_board)
    mcp.add_tool(board.get_boards)

    # List Tools
    mcp.add_tool(list.get_list)
    mcp.add_tool(list.get_lists)
    mcp.add_tool(list.create_list)
    mcp.add_tool(list.update_list)
    mcp.add_tool(list.delete_list)

    # Card Tools
    mcp.add_tool(card.get_card)
    mcp.add_tool(card.get_cards)
    mcp.add_tool(card.create_card)
    mcp.add_tool(card.update_card)
    mcp.add_tool(card.delete_card)
