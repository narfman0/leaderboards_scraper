import json
import logging
import requests

from leaderboards_scraper.models import Run
from leaderboards_scraper.src_api import (
    download_category_runs,
    SRC_CATEGORIES,
)


def main():
    logging.basicConfig(filename="leaderboards.log", level=logging.INFO)
    # we want to decouple api json requests and generating websites, while doing this cheaply
    # 1. download all /runs locally with respectful/stealth mode invocation
    for category in SRC_CATEGORIES:
        download_category_runs(category)

    # 2. have system to generate markdown from local runs json
    # 3. git add markdown to jekyll website, commit, push, let static site generation solve everything?
    # followon work
    # * populate database from json to enrich run information
    # * enumerate games and categories to scrape
    pass


if __name__ == "__main__":
    # execute only if run as a script
    main()