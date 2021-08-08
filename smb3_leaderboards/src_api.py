import json
import logging
from os.path import exists
import random
import requests
import time

from pydantic.dataclasses import dataclass
from pydantic.json import pydantic_encoder

from smb3_leaderboards.models import Run

SRC_API_ROOT = "https://www.speedrun.com/api/v1"
SRC_API_RUNS = SRC_API_ROOT + "/runs?max=200&category="
SRC_SMB3_GAME_ID = "l3dx51yv"
SRC_SMB3_WARPLESS_CATEGORY_ID = "rklxwwkn"
SRC_SMB3_HUNDO_CATEGORY_ID = "7dg8z424"
SRC_SMB3_NWW_CATEGORY_ID = "ndxjyj2q"
SRC_SMB3_ANY_CATEGORY_ID = "wkpjpvkr"


def process_category_runs_page(category_id, url, page_number):
    if not does_raw_file_exists(category_id, page_number):
        response_json = make_request(category_id, page_number, url)
        store_raw_category_runs_page(category_id, page_number, response_json)
    else:
        response_json = load_raw_file_json(category_id, page_number)
    runs = parse_category_runs_page(response_json["data"])
    store_parsed_category_runs_page(category_id, page_number, runs)
    trigger_next_request(category_id, page_number, response_json)


def trigger_next_request(category_id, page_number, response_json):
    for link in response_json["pagination"]["links"]:
        if link["rel"] == "next":
            next_uri = link["uri"]
            logging.info(
                f"Found next_url {next_uri} for category {category_id} page {page_number}"
            )
            process_category_runs_page(category_id, next_uri, page_number + 1)


def load_raw_file_json(category_id, page_number):
    # store in database to compare if runs are updated? maybe later
    with open(f"data/raw_{category_id}_{page_number}.json") as file:
        result = json.loads(file.read())
        logging.info(f"Read raw category {category_id} page {page_number}")
        return result


def make_request(category_id, page_number, url):
    # cautiously wait between 1-2 hours before next call
    time.sleep(60 * 60 + random.randint(0, 60 * 60))
    logging.info(f"Making request for category {category_id} page {page_number}")
    r = requests.get(url)
    if r.status_code != 200:
        log_string = (
            f"Failed to download {url} for category {category_id} page {page_number}"
        )
        logging.warning(log_string)
        raise Exception(log_string)
    return r.json()


def store_parsed_category_runs_page(category_id, page_number, runs):
    with open(f"data/parsed_{category_id}_{page_number}.json", "w") as file:
        file.write(json.dumps(runs, default=pydantic_encoder))
        logging.info(f"Wrote parsed category {category_id} page {page_number}")


def store_raw_category_runs_page(category_id, page_number, runs_page):
    # store in database to compare if runs are updated? maybe later
    with open(f"data/raw_{category_id}_{page_number}.json", "w") as file:
        file.write(json.dumps(runs_page))
        logging.info(f"Wrote raw category {category_id} page {page_number}")


def does_raw_file_exists(category_id, page_number):
    return exists(f"data/raw_{category_id}_{page_number}.json")


def parse_category_runs_page(runs_json):
    runs = []
    for run_json in runs_json:
        run = run_from_src_api_json(run_json)
        if run:
            runs.append(run)
    return runs


def download_category_runs(category_id):
    process_category_runs_page(
        category_id,
        f"{SRC_API_RUNS}{SRC_SMB3_WARPLESS_CATEGORY_ID}",
        0,
    )


def run_from_src_api_json(run_json):
    run_id = run_json["id"]
    try:
        player_ids = []
        for player in run_json["players"]:
            if "id" in player:
                player_ids.append(player["id"])
            else:
                logging.info(f"Player found without id: {player}")
        return Run(
            id=run_id,
            player_ids=player_ids,
            category_id=run_json["category"],
            video_url=run_json["videos"]["links"][0]["uri"],
            comment=run_json["comment"],
            date=run_json["date"],
            time=run_json["times"].get("realtime_t"),
            splits_io_url=(run_json["splits"] or {}).get("uri"),
        )
    except Exception as e:
        logging.warning(f"Exception {e} received for run_id {run_id}")