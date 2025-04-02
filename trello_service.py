# trello_api.py
from trello_api import TrelloClient

from typing import Dict, List, Any
from models import TrelloBoard, TrelloList, TrelloCard

TRELLO_API_BASE = "https://api.trello.com/1"


class TrelloService:
    def __init__(self, api_key: str, token: str):
        """Initializes the Trello client with API key and token."""
        self.client = TrelloClient(api_key, token)

    async def close(self) -> None:
        """Closes the underlying HTTP client."""
        await self.client.close()

    # Boards
    async def get_board(self, board_id: str) -> TrelloBoard:
        """Retrieves a specific board by its ID.

        Args:
            board_id (str): The ID of the board to retrieve.

        Returns:
            TrelloBoard: The board object containing board details.
        """
        response = await self.client._get(f"/boards/{board_id}")
        return TrelloBoard(**response)

    async def get_boards(self, member_id: str = "me") -> List[TrelloBoard]:
        """Retrieves all boards for a given member.

        Args:
            member_id (str): The ID of the member whose boards to retrieve. Defaults to "me" for the authenticated user.

        Returns:
            List[TrelloBoard]: A list of board objects.
        """
        response = await self.client._get(f"/members/{member_id}/boards")
        return [TrelloBoard(**board) for board in response]

    # Lists
    async def get_list(self, list_id: str) -> TrelloList:
        """Retrieves a specific list by its ID.

        Args:
            list_id (str): The ID of the list to retrieve.

        Returns:
            TrelloList: The list object containing list details.
        """
        response = await self.client._get(f"/lists/{list_id}")
        return TrelloList(**response)

    async def get_lists(self, board_id: str) -> List[TrelloList]:
        """Retrieves all lists on a given board.

        Args:
            board_id (str): The ID of the board whose lists to retrieve.

        Returns:
            List[TrelloList]: A list of list objects.
        """
        response = await self.client._get(f"/boards/{board_id}/lists")
        return [TrelloList(**list_data) for list_data in response]

    async def update_list(self, list_id: str, name: str) -> TrelloList:
        """Updates the name of a list.

        Args:
            list_id (str): The ID of the list to update.
            name (str): The new name for the list.

        Returns:
            TrelloList: The updated list object.
        """
        response = await self.client._put(f"/lists/{list_id}", data={"name": name})
        return TrelloList(**response)

    async def delete_list(self, list_id: str) -> TrelloList:
        """Archives a list.

        Args:
            list_id (str): The ID of the list to close.

        Returns:
            TrelloList: The archived list object.
        """
        response = await self.client._put(
            f"/lists/{list_id}/closed", data={"value": "true"}
        )
        return TrelloList(**response)

    # Cards
    async def get_card(self, card_id: str) -> TrelloCard:
        """Retrieves a specific card by its ID.

        Args:
            card_id (str): The ID of the card to retrieve.

        Returns:
            TrelloCard: The card object containing card details.
        """
        response = await self.client._get(f"/cards/{card_id}")
        return TrelloCard(**response)

    async def get_cards(self, list_id: str) -> List[TrelloCard]:
        """Retrieves all cards in a given list.

        Args:
            list_id (str): The ID of the list whose cards to retrieve.

        Returns:
            List[TrelloCard]: A list of card objects.
        """
        response = await self.client._get(f"/lists/{list_id}/cards")
        return [TrelloCard(**card) for card in response]

    async def create_card(
        self, list_id: str, name: str, desc: str = None
    ) -> TrelloCard:
        """Creates a new card in a given list.

        Args:
            list_id (str): The ID of the list to create the card in.
            name (str): The name of the new card.
            desc (str, optional): The description of the new card. Defaults to None.

        Returns:
            TrelloCard: The newly created card object.
        """
        data = {"name": name, "idList": list_id}
        if desc:
            data["desc"] = desc
        response = await self.client._post(f"/cards", data=data)
        return TrelloCard(**response)

    async def update_card(self, card_id: str, **kwargs) -> TrelloCard:
        """Updates a card's attributes.

        Args:
            card_id (str): The ID of the card to update.
            **kwargs: Keyword arguments representing the attributes to update on the card.

        Returns:
            TrelloCard: The updated card object.
        """
        response = await self.client._put(f"/cards/{card_id}", data=kwargs)
        return TrelloCard(**response)

    async def delete_card(self, card_id: str) -> Dict[str, Any]:
        """Deletes a card.

        Args:
            card_id (str): The ID of the card to delete.

        Returns:
            Dict[str, Any]: The response from the delete operation.
        """
        return await self.client._delete(f"/cards/{card_id}")
