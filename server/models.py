from typing import Optional

from pydantic import BaseModel


class TrelloBoard(BaseModel):
    """Model representing a Trello board."""

    id: str
    name: str
    desc: Optional[str] = None
    closed: bool = False
    idOrganization: Optional[str] = None
    url: str


class TrelloList(BaseModel):
    """Model representing a Trello list."""

    id: str
    name: str
    closed: bool = False
    idBoard: str
    pos: float


class TrelloCard(BaseModel):
    """Model representing a Trello card."""

    id: str
    name: str
    desc: Optional[str] = None
    closed: bool = False
    idList: str
    idBoard: str
    url: str
    pos: float
