from pydantic import BaseModel


class UpdateCardPayload(BaseModel):
    """
    Payload for updating a card.

    Attributes:
        name (str): The name of the card.
        desc (str): The description of the card.
        pos (str | int): The position of the card.
        closed (bool): Whether the card is closed or not.
        due (str): The due date of the card in ISO 8601 format.
        dueComplete (bool): Whether the due date is marked as complete.
        idLabels (str): Comma-separated list of label IDs for the card.
    """

    name: str | None = None
    desc: str | None = None
    pos: str | None = None
    closed: bool | None = None
    due: str | None = None
    dueComplete: bool | None = None
    idLabels: str | None = None
