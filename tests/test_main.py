import json
import unittest
from smb3_leaderboards import main


class TestMain(unittest.TestCase):
    def test_logic(self):
        self.assertEqual("Hello World!", main.logic())

    def test_store_category_runs_page(self):
        with open("tests/fixtures/smb3HundoRuns1.json") as file:
            content = file.read()
            content_json = json.loads(content)
            main.store_category_runs_page("abc123", 0, content_json["data"])