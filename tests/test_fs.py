import json
import unittest
from leaderboards_scraper import fs


class TestFs(unittest.TestCase):
    def test_store_raw_category_runs_page(self):
        with open("tests/fixtures/smb3HundoRuns1.json") as file:
            content = file.read()
            content_json = json.loads(content)
            fs.store_raw_category_runs_page("abc123", 0, content_json["data"])
