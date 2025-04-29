from typing import List

from models import TrelloBoard
from trello_api import TrelloClient


class BoardService:
    def __init__(self, client: TrelloClient):
        self.client = client

    async def get_board(self, board_id: str) -> TrelloBoard:
        """Retrieves a specific board by its ID.

        Args:
            board_id (str): The ID of the board to retrieve.

        Returns:
            TrelloBoard: The board object containing board details.
        """
        response = await self.client.GET(f"/boards/{board_id}")
        return TrelloBoard(**response)

    async def get_boards(self, member_id: str = "me") -> List[TrelloBoard]:
        """Retrieves all boards for a given member.

        Args:
            member_id (str): The ID of the member whose boards to retrieve. Defaults to "me" for the authenticated user.

        Returns:
            List[TrelloBoard]: A list of board objects.
        """
        response = await self.client.GET(f"/members/{member_id}/boards")
        return [TrelloBoard(**board) for board in response]
