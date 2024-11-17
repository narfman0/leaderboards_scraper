from pydantic import BaseModel


class Player(BaseModel):
    id: str | None = None
    name: str | None = None


class Run(BaseModel):
    """Class for keeping track of a run."""

    id: str
    players: list[Player]
    category_id: str
    date: str
    time: float  # seconds
    status: str
    video_url: str | None = None
    comment: str | None = None
    splits_io_url: str | None = None


class Game(BaseModel):
    id: str
    name: str


class Category(BaseModel):
    id: str
    name: str
