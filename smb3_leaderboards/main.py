import json
import logging
import requests

from smb3_leaderboards.models import Run
from smb3_leaderboards.src_api import download_category_runs


def logic():
    # we want to decouple api json requests and generating websites, while doing this cheaply
    # 1. download all /runs locally with respectful/stealth mode invocation
    # download_category_runs()

    # 2. have system to generate markdown from local runs json
    # 3. git add markdown to jekyll website, commit, push, let static site generation solve everything?
    # followon work
    # * populate database from json to enrich run information
    # * enumerate games and categories to scrape
    return "Hello World!"