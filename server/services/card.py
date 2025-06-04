"""
Service for managing Trello cards in MCP server.
"""

from typing import Any, Dict, List

from server.models import TrelloCard, TrelloComment
from server.utils.trello_api import TrelloClient


class CardService:
    """
    Service class for managing Trello cards.
    """

    def __init__(self, client: TrelloClient):
        self.client = client

    async def get_card(self, card_id: str) -> TrelloCard:
        """Retrieves a specific card by its ID.

        Args:
            card_id (str): The ID of the card to retrieve.

        Returns:
            TrelloCard: The card object containing card details.
        """
        params = {"actions": "commentCard"}
        response = await self.client.GET(f"/cards/{card_id}", params=params)
        
        # Parse comments from actions
        comments = self._parse_comments(response.get("actions", []))
        
        card_data = response
        card_data["comments"] = comments
        return TrelloCard(**card_data)

    async def get_cards(self, list_id: str) -> List[TrelloCard]:
        """Retrieves all cards in a given list.

        Args:
            list_id (str): The ID of the list whose cards to retrieve.

        Returns:
            List[TrelloCard]: A list of card objects.
        """
        response = await self.client.GET(f"/lists/{list_id}/cards")
        return [TrelloCard(**card) for card in response]

    async def create_card(self, **kwargs) -> TrelloCard:
        """Creates a new card in a given list.

        Args
            list_id (str): The ID of the list to create the card in.
            name (str): The name of the new card.
            desc (str, optional): The description of the new card. Defaults to None.

        Returns:
            TrelloCard: The newly created card object.
        """
        response = await self.client.POST("/cards", data=kwargs)
        return TrelloCard(**response)

    async def update_card(self, card_id: str, **kwargs) -> TrelloCard:
        """Updates a card's attributes.

        Args:
            card_id (str): The ID of the card to update.
            **kwargs: Keyword arguments representing the attributes to update on the card.

        Returns:
            TrelloCard: The updated card object.
        """
        response = await self.client.PUT(f"/cards/{card_id}", data=kwargs)
        return TrelloCard(**response)

    async def delete_card(self, card_id: str) -> Dict[str, Any]:
        """Deletes a card.

        Args:
            card_id (str): The ID of the card to delete.

        Returns:
            Dict[str, Any]: The response from the delete operation.
        """
        return await self.client.DELETE(f"/cards/{card_id}")

    def _parse_comments(self, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse comments from Trello actions.

        Args:
            actions (List[Dict[str, Any]]): List of Trello actions.

        Returns:
            List[Dict[str, Any]]: List of parsed comments.
        """
        comments = []
        for action in actions:
            if action.get("type") == "commentCard":
                comment_data = action.get("data", {}).get("text", "")
                comments.append({
                    "id": action.get("id"),
                    "author_id": action.get("idMemberCreator"),
                    "date": action.get("date"),
                    "text": comment_data
                })
        return comments
