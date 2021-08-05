import json
import logging
import requests

from pydantic.json import pydantic_encoder

from smb3_leaderboards.models import Run

SRC_API_ROOT = "https://www.speedrun.com/api/v1"
SRC_API_RUNS = SRC_API_ROOT + "/runs?max=200&category="
SRC_SMB3_GAME_ID = "l3dx51yv"
SRC_SMB3_WARPLESS_CATEGORY_ID = "rklxwwkn"
SRC_SMB3_HUNDO_CATEGORY_ID = "7dg8z424"
SRC_SMB3_NWW_CATEGORY_ID = "ndxjyj2q"
SRC_SMB3_ANY_CATEGORY_ID = "wkpjpvkr"


def download_category_runs_page(category_id, url, page_number):
    r = requests.get(url)
    if r.status_code != 200:
        logging.warning("Failed to download " + category_id)
    store_category_runs_page(category_id, page_number, r.json["data"])
    next_url = r.json["pagination"]["links"][0]["uri"]
    if next_url:
        download_category_runs_page(category_id, next_url, page_number + 1)


def store_category_runs_page(category_id, page_number, runs_page):
    # store in database to compare if runs are updated? maybe later
    with open(f"data/raw_{category_id}_{page_number}.json", "w") as file:
        file.write(json.dumps(runs_page))
    runs = []
    for run_json in runs_page:
        run = run_from_src_api_json(run_json)
        runs.append(run)
    with open(f"data/parsed_{category_id}_{page_number}.json", "w") as file:
        file.write(json.dumps(runs, default=pydantic_encoder))


def download_category_runs(category_id):
    download_category_runs_page(
        category_id, f"{SRC_API_RUNS}{SRC_SMB3_WARPLESS_CATEGORY_ID}", 0
    )


def run_from_src_api_json(run_json):
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