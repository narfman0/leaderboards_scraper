import json
import logging
import os

from pydantic.json import pydantic_encoder

from leaderboards_scraper.models import Category, Player, Run

PLAYERS_JSON_PATH = "data/players/parsed_players.json"
CATEGORIES_JSON_PATH = "data/categories/smb3.json"


def does_raw_run_exist(category_id, page_number):
    return os.path.exists(f"data/runs/raw_{category_id}_{page_number}.json")


def does_raw_player_exist(player_id):
    return os.path.exists(f"data/players/raw_{player_id}.json")


def load_raw_player_json(player_id):
    with open(f"data/players/raw_{player_id}.json") as file:
        result = json.loads(file.read())
        logging.info(f"Read raw player {player_id}")
        return result


def load_raw_run_json(category_id, page_number):
    # store in database to compare if runs are updated? maybe later
    with open(f"data/runs/raw_{category_id}_{page_number}.json") as file:
        result = json.loads(file.read())
        logging.info(f"Read raw category {category_id} page {page_number}")
        return result


def load_categories(categories_json_path=CATEGORIES_JSON_PATH):
    if not os.path.exists(categories_json_path):
        return []
    with open(categories_json_path) as file:
        result = json.loads(file.read())
        categories = []
        for result_item in result["data"]:
            categories.append(Category(result_item["id"], result_item["name"]))
        logging.info(f"Read {len(categories)} categories")
        return categories


def load_parsed_players(players_json_path=PLAYERS_JSON_PATH):
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


def store_parsed_runs(category_id, runs):
    with open(f"data/runs/parsed_{category_id}_runs.json", "w") as file:
        file.write(json.dumps(runs, default=pydantic_encoder))
        logging.info(f"Wrote parsed {len(runs)} {category_id} runs")


def store_parsed_players(players):
    with open(PLAYERS_JSON_PATH, "w") as file:
        file.write(json.dumps(players, default=pydantic_encoder))
        logging.info(f"Wrote {len(players)} parsed players")


def store_raw_category_runs_page(category_id, page_number, runs_page):
    # store in database to compare if runs are updated? maybe later
    with open(f"data/runs/raw_{category_id}_{page_number}.json", "w") as file:
        file.write(json.dumps(runs_page))
        logging.info(f"Wrote raw category {category_id} page {page_number}")


def store_raw_player(player_id, player_data):
    with open(f"data/players/raw_{player_id}.json", "w") as file:
        file.write(json.dumps(player_data))
        logging.info(f"Wrote raw player {player_id}")


def store_category_leaderboard(category_id, markdown):
    with open(f"data/leaderboards/{category_id}.md", "w") as file:
        file.write(markdown)
        logging.info(f"Wrote category leaderboard {category_id}")
