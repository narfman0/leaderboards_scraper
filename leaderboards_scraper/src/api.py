import logging

from leaderboards_scraper.fs import (
    does_raw_player_exist,
    does_raw_run_exist,
    load_parsed_runs,
    load_parsed_players,
    load_raw_run_json,
    load_raw_player_json,
    store_parsed_category_runs_page,
    store_parsed_players,
    store_raw_category_runs_page,
    store_raw_player,
)
from leaderboards_scraper.src.parser import parse_category_runs_page, parse_player
from leaderboards_scraper.web import get_json_from_url

SRC_API_ROOT = "https://www.speedrun.com/api/v1"
SRC_API_RUNS = SRC_API_ROOT + "/runs?max=200&category="
SRC_API_USER = SRC_API_ROOT + "/users/"
SRC_SMB3_GAME_ID = "l3dx51yv"
SRC_SMB3_WARPLESS_CATEGORY_ID = "rklxwwkn"
SRC_SMB3_HUNDO_CATEGORY_ID = "7dg8z424"
SRC_SMB3_NWW_CATEGORY_ID = "ndxjyj2q"
SRC_SMB3_ANY_CATEGORY_ID = "wkpjpvkr"
SRC_SMB3_CATEGORY_IDS = [
    SRC_SMB3_WARPLESS_CATEGORY_ID,
    SRC_SMB3_HUNDO_CATEGORY_ID,
    SRC_SMB3_NWW_CATEGORY_ID,
    SRC_SMB3_ANY_CATEGORY_ID,
]


def process_category_runs_page(category_id, url, page_number):
    if not does_raw_run_exist(category_id, page_number):
        response_json = get_json_from_url(category_id, page_number, url)
        store_raw_category_runs_page(category_id, page_number, response_json)
    else:
        response_json = load_raw_run_json(category_id, page_number)
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


def process_category_runs(category_id):
    process_category_runs_page(
        category_id, f"{SRC_API_RUNS}{category_id}", 0,
    )


def process_runs():
    for category_id in SRC_SMB3_CATEGORY_IDS:
        process_category_runs_page(
            category_id, f"{SRC_API_RUNS}{category_id}", 0,
        )


def process_players():
    # all players in available runs
    runs = load_parsed_runs()
    run_player_ids = set()
    for run in runs:
        run_player_ids = run_player_ids.union(run.player_ids)
    # all players stored locally
    local_player_ids = set([player.id for player in load_parsed_players()])
    unknown_player_ids = run_player_ids - local_player_ids
    players = []
    for unknown_player_id in unknown_player_ids:
        if not does_raw_player_exist(unknown_player_id):
            response_json = get_json_from_url(SRC_API_USER + unknown_player_id)
            store_raw_player(unknown_player_id, response_json)
        else:
            response_json = load_raw_player_json(unknown_player_id)
        players.append(parse_player(response_json["data"]))
    store_parsed_players(players)
