import logging
from typing import Dict, List, Optional

from server.utils.trello_api import TrelloClient

logger = logging.getLogger(__name__)


class ChecklistService:
    """
    Service class for handling Trello checklist operations.
    """

    def __init__(self, client: TrelloClient):
        self.client = client

    async def get_checklist(self, checklist_id: str) -> Dict:
        """
        Get a specific checklist by ID.

        Args:
            checklist_id (str): The ID of the checklist to retrieve

        Returns:
            Dict: The checklist data
        """
        return await self.client.GET(f"/checklists/{checklist_id}")

    async def get_card_checklists(self, card_id: str) -> List[Dict]:
        """
        Get all checklists for a specific card.

        Args:
            card_id (str): The ID of the card to get checklists for

        Returns:
            List[Dict]: List of checklists on the card
        """
        return await self.client.GET(f"/cards/{card_id}/checklists")

    async def create_checklist(
        self, card_id: str, name: str, pos: Optional[str] = None
    ) -> Dict:
        """
        Create a new checklist on a card.

        Args:
            card_id (str): The ID of the card to create the checklist on
            name (str): The name of the checklist
            pos (Optional[str]): The position of the checklist (top, bottom, or a positive number)

        Returns:
            Dict: The created checklist data
        """
        data = {"name": name}
        if pos:
            data["pos"] = pos
        return await self.client.POST("/checklists", data={"idCard": card_id, **data})

    async def update_checklist(
        self, checklist_id: str, name: Optional[str] = None, pos: Optional[str] = None
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
        data = {}
        if name:
            data["name"] = name
        if pos:
            data["pos"] = pos
        return await self.client.PUT(f"/checklists/{checklist_id}", data=data)

    async def delete_checklist(self, checklist_id: str) -> Dict:
        """
        Delete a checklist.

        Args:
            checklist_id (str): The ID of the checklist to delete

        Returns:
            Dict: The response from the delete operation
        """
        return await self.client.DELETE(f"/checklists/{checklist_id}")

    async def add_checkitem(
        self,
        checklist_id: str,
        name: str,
        checked: bool = False,
        pos: Optional[str] = None,
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
        data = {"name": name, "checked": checked}
        if pos:
            data["pos"] = pos
        return await self.client.POST(
            f"/checklists/{checklist_id}/checkItems", data=data
        )

    async def update_checkitem(
        self,
        checklist_id: str,
        checkitem_id: str,
        name: Optional[str] = None,
        checked: Optional[bool] = None,
        pos: Optional[str] = None,
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
        data = {}
        if name:
            data["name"] = name
        if checked is not None:
            data["checked"] = checked
        if pos:
            data["pos"] = pos
        return await self.client.PUT(
            f"/checklists/{checklist_id}/checkItems/{checkitem_id}", data=data
        )

    async def delete_checkitem(self, checklist_id: str, checkitem_id: str) -> Dict:
        """
        Delete a checkitem from a checklist.

        Args:
            checklist_id (str): The ID of the checklist containing the item
            checkitem_id (str): The ID of the checkitem to delete

        Returns:
            Dict: The response from the delete operation
        """
        return await self.client.DELETE(
            f"/checklists/{checklist_id}/checkItems/{checkitem_id}"
        )
