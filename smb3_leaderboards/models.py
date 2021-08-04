from dataclasses import dataclass
from typing import List


@dataclass
class Run:
    """Class for keeping track of a run."""

    id: str
    player_ids: List[str]
    category_id: str
    date: str
    comment: str
    video_url: str
    time: int  # seconds
    splits_io_url: str

    def from_src_api_json(run_json):
        player_ids = []
        for player in run_json["players"]:
            player_ids.append(player["id"])
        return Run(
            id=run_json["id"],
            player_ids=player_ids,
            category_id=run_json["category"],
            video_url=run_json["videos"]["links"][0]["uri"],
            comment=run_json["comment"],
            date=run_json["date"],
            time=run_json["times"].get("realtime_t"),
            splits_io_url=(run_json["splits"] or {}).get("uri"),
        )


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