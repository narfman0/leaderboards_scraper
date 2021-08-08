from typing import List

from pydantic.dataclasses import dataclass


@dataclass
class Run:
    """Class for keeping track of a run."""

    id: str
    player_ids: List[str]
    category_id: str
    date: str
    video_url: str
    time: int  # seconds
    comment: str = None
    splits_io_url: str = None


@dataclass
class Player:
    id: str
    name: str


@dataclass
class Game:
    id: str
    name: str


@dataclass
class Category:
    id: str
    name: str