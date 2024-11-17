import logging
import random

from leaderboards_scraper.fs import (
    does_raw_player_exist,
    does_raw_run_exist,
    load_categories,
    load_parsed_runs,
    load_parsed_players,
    load_raw_run_json,
    load_raw_player_json,
    store_parsed_category_runs_page,
    store_parsed_players,
    store_parsed_runs,
    store_raw_category_runs_page,
    store_raw_player,
)
from leaderboards_scraper.src.parser import parse_category_runs_page, parse_raw_player
from leaderboards_scraper.web import get_json_from_url

SRC_API_ROOT = "https://www.speedrun.com/api/v1"
SRC_API_RUNS = SRC_API_ROOT + "/runs?max=200&category="
SRC_API_USER = SRC_API_ROOT + "/users/"


def process_category_runs_page(category_id, url, page_number, runs):
    if not does_raw_run_exist(category_id, page_number):
        response_json = get_json_from_url(url)
        store_raw_category_runs_page(category_id, page_number, response_json)
    else:
        response_json = load_raw_run_json(category_id, page_number)
    parsed_runs = parse_category_runs_page(response_json["data"])
    store_parsed_category_runs_page(category_id, page_number, parsed_runs)
    runs.extend(parsed_runs)
    trigger_next_request(category_id, page_number, response_json, runs)


def trigger_next_request(category_id, page_number, response_json, runs):
    for link in response_json["pagination"]["links"]:
        if link["rel"] == "next":
            next_uri = link["uri"]
            logging.info(
                f"Found next_url {next_uri} for category {category_id} page {page_number}"
            )
            process_category_runs_page(category_id, next_uri, page_number + 1, runs)


def process_runs():
    category_to_runs = {}
    categories = load_categories()
    random.shuffle(categories)
    for category in categories:
        try:
            runs = load_parsed_runs(category.id)
            process_category_runs_page(
                category.id,
                f"{SRC_API_RUNS}{category.id}",
                0,
                runs,
            )
            runs = list({run.id: run for run in runs}.values())  # deduplicate
            store_parsed_runs(category.id, runs)
            category_to_runs[category.id] = runs
        except Exception as e:
            logging.error(f"Failed to process category {category.id} with error {e}")
            raise e
    return category_to_runs


def process_players():
    # all players in available runs
    runs = load_parsed_runs()
    run_player_ids = set()
    for run in runs:
        run_player_ids = run_player_ids.union([player.id for player in run.players])
    # all players stored locally
    parsed_players = load_parsed_players()
    local_player_ids = set([player.id for player in parsed_players])
    unknown_player_ids = run_player_ids - local_player_ids
    for unknown_player_id in unknown_player_ids:
        try:
            if not does_raw_player_exist(unknown_player_id):
                response_json = get_json_from_url(SRC_API_USER + unknown_player_id)
                if not response_json:
                    logging.warning(
                        f"Response json null for player {unknown_player_id}, skipping"
                    )
                    continue
                store_raw_player(unknown_player_id, response_json)
            else:
                response_json = load_raw_player_json(unknown_player_id)
            parsed_players.append(parse_raw_player(response_json["data"]))
        except Exception as e:
            logging.warning(e)
            raise e
    store_parsed_players(parsed_players)
    return {player.id: player for player in parsed_players}
