from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

from pydantic import BaseModel, Field


class TrelloLabel(BaseModel):
    """Model representing a Trello label."""
    id: str
    idBoard: str
    name: str
    color: Optional[str] = None
    uses: Optional[int] = None


class TrelloBoard(BaseModel):
    """Model representing a Trello board."""

    id: str
    name: str
    desc: Optional[str] = None
    closed: bool = False
    idOrganization: Optional[str] = None
    url: str
    shortUrl: Optional[str] = None
    prefs: Optional[Dict[str, Any]] = None
    labelNames: Optional[Dict[str, str]] = None
    starred: Optional[bool] = None
    subscribed: Optional[bool] = None
    dateLastActivity: Optional[datetime] = None
    dateLastView: Optional[datetime] = None
    shortLink: Optional[str] = None


class TrelloList(BaseModel):
    """Model representing a Trello list."""

    id: str
    name: str
    closed: bool = False
    idBoard: str
    pos: float # Or str for "top"/"bottom" in some contexts, Trello API is flexible
    subscribed: Optional[bool] = None
    softLimit: Optional[str] = None # Or int/float, or a more complex object


class TrelloCard(BaseModel):
    """Model representing a Trello card."""

    id: str
    name: str
    desc: Optional[str] = None
    closed: bool = False
    idList: str
    idBoard: str
    url: str
    pos: float # Or str for "top"/"bottom" in some contexts
    dateLastActivity: Optional[datetime] = None
    labels: List[TrelloLabel] = Field(default_factory=list)
    idLabels: List[str] = Field(default_factory=list)
    due: Optional[datetime] = None
    start: Optional[datetime] = None
    dueComplete: Optional[bool] = None
    idChecklists: List[str] = Field(default_factory=list)
    idMembers: List[str] = Field(default_factory=list)
    shortLink: Optional[str] = None
    idAttachmentCover: Optional[str] = None
    cover: Optional[Dict[str, Any]] = None # Can be a more specific model
    badges: Optional[Dict[str, Any]] = None # Can be a more specific model
    subscribed: Optional[bool] = None

    @property
    def creationDate(self) -> Optional[datetime]:
        if self.id and len(self.id) == 24:  # Standard MongoDB ObjectId length
            try:
                timestamp_hex = self.id[:8]
                timestamp_int = int(timestamp_hex, 16)
                return datetime.fromtimestamp(timestamp_int, tz=timezone.utc)
            except ValueError:
                return None
        return None
