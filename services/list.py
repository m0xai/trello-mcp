from typing import List

from models import TrelloList
from trello_api import TrelloClient


class ListService:
    """
    Service class for managing Trello lists.
    """

    def __init__(self, client: TrelloClient):
        self.client = client

    # Lists
    async def get_list(self, list_id: str) -> TrelloList:
        """Retrieves a specific list by its ID.

        Args:
            list_id (str): The ID of the list to retrieve.

        Returns:
            TrelloList: The list object containing list details.
        """
        response = await self.client.GET(f"/lists/{list_id}")
        return TrelloList(**response)

    async def get_lists(self, board_id: str) -> List[TrelloList]:
        """Retrieves all lists on a given board.

        Args:
            board_id (str): The ID of the board whose lists to retrieve.

        Returns:
            List[TrelloList]: A list of list objects.
        """
        response = await self.client.GET(f"/boards/{board_id}/lists")
        return [TrelloList(**list_data) for list_data in response]

    async def create_list(
        self, board_id: str, name: str, pos: str = "bottom"
    ) -> TrelloList:
        """Creates a new list on a given board.

        Args:
            board_id (str): The ID of the board to create the list in.
            name (str): The name of the new list.
            pos (str, optional): The position of the new list. Can be "top" or "bottom". Defaults to "bottom".

        Returns:
            TrelloList: The newly created list object.
        """
        data = {"name": name, "idBoard": board_id, "pos": pos}
        response = await self.client.POST("/lists", data=data)
        return TrelloList(**response)

    async def update_list(self, list_id: str, name: str) -> TrelloList:
        """Updates the name of a list.

        Args:
            list_id (str): The ID of the list to update.
            name (str): The new name for the list.

        Returns:
            TrelloList: The updated list object.
        """
        response = await self.client.PUT(f"/lists/{list_id}", data={"name": name})
        return TrelloList(**response)

    async def delete_list(self, list_id: str) -> TrelloList:
        """Archives a list.

        Args:
            list_id (str): The ID of the list to close.

        Returns:
            TrelloList: The archived list object.
        """
        response = await self.client.PUT(
            f"/lists/{list_id}/closed", data={"value": "true"}
        )
        return TrelloList(**response)
