import json
import logging
import requests

from smb3_leaderboards.models import Run

SRC_API_ROOT = "https://www.speedrun.com/api/v1"
SRC_API_RUNS = SRC_API_ROOT + "/runs?category="
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
    with open(f"data/{category_id}_{page_number}.json", "w") as file:
        file.write(json.dumps(runs_page))
    runs = []
    for run_json in runs_page:
        run = Run.from_src_api_json(run_json)
        breakpoint()
        runs.append(run)


def download_category_runs(category_id):
    download_category_runs_page(
        category_id, f"{SRC_API_RUNS}{SRC_SMB3_WARPLESS_CATEGORY_ID}", 0
    )


def logic():
    # we want to decouple api json requests and generating websites, while doing this cheaply
    # 1. download all /runs locally with respectful/stealth mode invocation
    # download_category_runs(SRC_SMB3_WARPLESS_CATEGORY_ID)

    # 2. have system to generate markdown from local runs json
    # 3. git add markdown to jekyll website, commit, push, let static site generation solve everything?
    # followon work
    # * populate database from json to enrich run information
    # * enumerate games and categories to scrape
    return "Hello World!"