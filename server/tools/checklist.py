"""
This module contains tools for managing Trello checklists.
"""

import logging
from typing import Dict, List

from server.services.checklist import ChecklistService
from server.trello import client

logger = logging.getLogger(__name__)
service = ChecklistService(client)


async def get_checklist(checklist_id: str) -> Dict:
    """
    Get a specific checklist by ID.

    Args:
        checklist_id (str): The ID of the checklist to retrieve

    Returns:
        Dict: The checklist data
    """
    return await service.get_checklist(checklist_id)


async def get_card_checklists(card_id: str) -> List[Dict]:
    """
    Get all checklists for a specific card.

    Args:
        card_id (str): The ID of the card to get checklists for

    Returns:
        List[Dict]: List of checklists on the card
    """
    return await service.get_card_checklists(card_id)


async def create_checklist(card_id: str, name: str, pos: str | None = None) -> Dict:
    """
    Create a new checklist on a card.

    Args:
        card_id (str): The ID of the card to create the checklist on
        name (str): The name of the checklist
        pos (Optional[str]): The position of the checklist (top, bottom, or a positive number)

    Returns:
        Dict: The created checklist data
    """
    return await service.create_checklist(card_id, name, pos)


async def update_checklist(
    checklist_id: str, name: str | None = None, pos: str | None = None
) -> Dict:
    """
    Update an existing checklist.

    Args:
        checklist_id (str): The ID of the checklist to update
        name (Optional[str]): New name for the checklist
        pos (Optional[str]): New position for the checklist

    Returns:
        Dict: The updated checklist data
    """
    return await service.update_checklist(checklist_id, name, pos)


async def delete_checklist(checklist_id: str) -> Dict:
    """
    Delete a checklist.

    Args:
        checklist_id (str): The ID of the checklist to delete

    Returns:
        Dict: The response from the delete operation
    """
    return await service.delete_checklist(checklist_id)


async def add_checkitem(
    checklist_id: str, name: str, checked: bool = False, pos: str | None = None
) -> Dict:
    """
    Add a new item to a checklist.

    Args:
        checklist_id (str): The ID of the checklist to add the item to
        name (str): The name of the checkitem
        checked (bool): Whether the item is checked
        pos (Optional[str]): The position of the item

    Returns:
        Dict: The created checkitem data
    """
    return await service.add_checkitem(checklist_id, name, checked, pos)


async def update_checkitem(
    checklist_id: str,
    checkitem_id: str,
    name: str | None = None,
    checked: bool | None = None,
    pos: str | None = None,
) -> Dict:
    """
    Update a checkitem in a checklist.

    Args:
        checklist_id (str): The ID of the checklist containing the item
        checkitem_id (str): The ID of the checkitem to update
        name (Optional[str]): New name for the checkitem
        checked (Optional[bool]): New checked state
        pos (Optional[str]): New position for the item

    Returns:
        Dict: The updated checkitem data
    """
    return await service.update_checkitem(
        checklist_id, checkitem_id, name, checked, pos
    )


async def delete_checkitem(checklist_id: str, checkitem_id: str) -> Dict:
    """
    Delete a checkitem from a checklist.

    Args:
        checklist_id (str): The ID of the checklist containing the item
        checkitem_id (str): The ID of the checkitem to delete

    Returns:
        Dict: The response from the delete operation
    """
    return await service.delete_checkitem(checklist_id, checkitem_id)
