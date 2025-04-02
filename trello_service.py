# trello_api.py
from trello_api import TrelloClient

TRELLO_API_BASE = "https://api.trello.com/1"

class TrelloService:
    def __init__(self, api_key: str, token: str):
        """Initializes the Trello client with API key and token."""
        self.client = TrelloClient(api_key, token)

    async def close(self):
        """Closes the underlying HTTP client."""
        await self.client.close()

    # Boards
    async def get_board(self, board_id: str):
        """Retrieves a specific board by its ID.

        Args:
            board_id (str): The ID of the board to retrieve.
        """
        return await self.client._get(f"/boards/{board_id}")

    async def get_boards(self, member_id: str = "me"):
        """Retrieves all boards for a given member.

        Args:
            member_id (str): The ID of the member whose boards to retrieve. Defaults to "me" for the authenticated user.
        """
        return await self.client._get(f"/members/{member_id}/boards")

    # Lists
    async def get_list(self, list_id: str):
        """Retrieves a specific list by its ID.

        Args:
            list_id (str): The ID of the list to retrieve.
        """
        return await self.client._get(f"/lists/{list_id}")

    async def get_lists(self, board_id: str):
        """Retrieves all lists on a given board.

        Args:
            board_id (str): The ID of the board whose lists to retrieve.
        """
        return await self.client._get(f"/boards/{board_id}/lists")
    
    async def update_list(self, list_id: str, name: str):
        """Updates the name of a list.

        Args:
            list_id (str): The ID of the list to update.
            name (str): The new name for the list.
        """
        return await self.client._put(f"/lists/{list_id}", data={"name": name})

    async def delete_list(self, list_id: str):
        """Archives a list.

        Args:
            list_id (str): The ID of the list to close.
        """
        return await self.client._put(f"/lists/{list_id}/closed", data={"value": "true"})

    # Cards
    async def get_card(self, card_id: str):
        """Retrieves a specific card by its ID.

        Args:
            card_id (str): The ID of the card to retrieve.
        """
        return await self.client._get(f"/cards/{card_id}")

    async def get_cards(self, list_id: str):
        """Retrieves all cards in a given list.

        Args:
            list_id (str): The ID of the list whose cards to retrieve.
        """
        return await self.client._get(f"/lists/{list_id}/cards")

    async def create_card(self, list_id: str, name: str, desc: str = None):
        """Creates a new card in a given list.

        Args:
            list_id (str): The ID of the list to create the card in.
            name (str): The name of the new card.
            desc (str, optional): The description of the new card. Defaults to None.
        """
        data = {"name": name, "idList": list_id}
        if desc:
            data["desc"] = desc
        return await self.client._post(f"/cards", data=data)

    async def update_card(self, card_id: str, **kwargs):
        """Updates a card's attributes.

        Args:
            card_id (str): The ID of the card to update.
            **kwargs: Keyword arguments representing the attributes to update on the card.
        """
        return await self.client._put(f"/cards/{card_id}", data=kwargs)

    async def delete_card(self, card_id: str):
        """Deletes a card.

        Args:
            card_id (str): The ID of the card to delete.
        """
        return await self.client._delete(f"/cards/{card_id}")
