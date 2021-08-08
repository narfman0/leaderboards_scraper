import json
import unittest
from smb3_leaderboards import src_api


class TestSrcApi(unittest.TestCase):
    def test_store_raw_category_runs_page(self):
        with open("tests/fixtures/smb3HundoRuns1.json") as file:
            content = file.read()
            content_json = json.loads(content)
            src_api.store_raw_category_runs_page("abc123", 0, content_json["data"])

    def test_store_parsed_category_runs_page(self):
        with open("data/raw_rklxwwkn_0.json") as file:
            content = file.read()
            content_json = json.loads(content)
            src_api.store_parsed_runs_page("abc123", 0, content_json["data"])