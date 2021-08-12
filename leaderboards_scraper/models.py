from typing import List

from pydantic.dataclasses import dataclass


@dataclass
class Player:
    id: str = None
    name: str = None


@dataclass
class Run:
    """Class for keeping track of a run."""

    id: str
    players: List[Player]
    category_id: str
    date: str
    time: float  # seconds
    status: str
    video_url: str = None
    comment: str = None
    splits_io_url: str = None


@dataclass
class Game:
    id: str
    name: str


@dataclass
class Category:
    id: str
    name: str
