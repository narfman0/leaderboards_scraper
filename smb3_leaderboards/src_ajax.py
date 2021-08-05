import json
import logging
import requests

from bs4 import BeautifulSoup

from smb3_leaderboards.models import Run

SRC_WARPLESS_CATEGORY_ID = 581
API_ROOT = "https://www.speedrun.com/ajax_leaderboard.php?vary=1628107622&timeunits=0&game=smb3&verified=1&region=&platform=&emulator=2&video=&obsolete=&date=&category="


def store_category_runs(category_id, html):
    # store in database to compare if runs are updated? maybe later
    with open(f"data/raw_ajax_{category_id}.html", "w") as file:
        file.write(html)
    soup = BeautifulSoup(html, "html.parser")
    runs = []
    for run_soup in soup.find_all("tr"):
        runs.append(run_from_src_ajax_soup(run_soup))


def download_category_runs(category_id=SRC_WARPLESS_CATEGORY_ID):
    if category_id != SRC_WARPLESS_CATEGORY_ID:
        logging.warning(
            "note: ajax download_category_runs only works for warpless, which might not be "
            + category_id
        )
        category_id = SRC_CATEGORY_ID
    r = requests.get(API_ROOT + category_id)
    if r.status_code != 200:
        logging.warning("Failed to download " + category_id)
    store_category_runs(category_id, r.body)


def run_from_src_ajax_soup(run_soup):
    if len(run_soup.find_all("th")) > 0:
        return None
    player_ids = [run_soup.select(".username-light")[0].string]
    return Run(
        id=run_soup["data-target"].split("/")[3],
        player_ids=player_ids,
        category_id="",  # TODO
        video_url="",  # TODO
        comment=run_soup["title"],
        date=run_soup.time["datetime"],
        time=111,  # TODO
    )