import json
import unittest
from leaderboards_scraper.src import api


class TestApi(unittest.TestCase):
    def test_process_players(self):
        with open("tests/fixtures/smb3HundoRuns1.json") as file:
            api.process_players()