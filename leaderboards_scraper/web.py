import logging
import os
import random
import requests
import time


def get_json_from_url(url):
    if "PYTEST_CURRENT_TEST" in os.environ:
        logging.warning("web get_json_from_url called from unit test, aborting")
        return
    # cautiously wait before next call
    time.sleep(random.randint(10, 20))
    logging.info(f"Making request for {url}")
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"Failed to download {url}")
    return r.json()
