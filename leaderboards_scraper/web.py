import logging
import random
import requests
import time


def get_json_from_url(url):
    # cautiously wait before next call
    time.sleep(10 + random.randint(0, 50))
    logging.info(f"Making request for {url}")
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"Failed to download {url}")
    return r.json()
