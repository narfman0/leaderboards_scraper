import json
import logging
import os

from pydantic.json import pydantic_encoder

from leaderboards_scraper.models import Player, Run

PLAYERS_JSON_PATH = "data/players.json"


def does_raw_run_exist(category_id, page_number):
    return os.path.exists(f"data/runs/raw_{category_id}_{page_number}.json")


def load_raw_run_json(category_id, page_number):
    # store in database to compare if runs are updated? maybe later
    with open(f"data/runs/raw_{category_id}_{page_number}.json") as file:
        result = json.loads(file.read())
        logging.info(f"Read raw category {category_id} page {page_number}")
        return result


def load_players(players_json_path=PLAYERS_JSON_PATH):
    if not os.path.exists(players_json_path):
        return []
    with open(players_json_path) as file:
        result = json.loads(file.read())
        players = []
        for result_item in result:
            players.append(Player(**result_item))
        logging.info(f"Read {len(players)} players")
        return players


def load_parsed_runs():
    runs = []
    for path in os.listdir("data/runs"):
        if path.startswith("parsed"):
            with open(f"data/runs/{path}") as file:
                run_dicts = json.loads(file.read())
                for run_dict in run_dicts:
                    try:
                        runs.append(Run(**run_dict))
                    except Exception as e:
                        logging.warning(
                            f"Failed to read run_dict entry {run_dict} with error {e}"
                        )
                logging.info(f"Read {len(run_dicts)} runs...")
    return runs


def store_parsed_category_runs_page(category_id, page_number, runs):
    with open(f"data/runs/parsed_{category_id}_{page_number}.json", "w") as file:
        file.write(json.dumps(runs, default=pydantic_encoder))
        logging.info(f"Wrote parsed category {category_id} page {page_number}")


def store_raw_category_runs_page(category_id, page_number, runs_page):
    # store in database to compare if runs are updated? maybe later
    with open(f"data/runs/raw_{category_id}_{page_number}.json", "w") as file:
        file.write(json.dumps(runs_page))
        logging.info(f"Wrote raw category {category_id} page {page_number}")