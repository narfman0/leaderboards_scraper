import unittest
from leaderboards_scraper.src import api


class TestApi(unittest.TestCase):
    def test_process_players(self):
        api.process_players()

    def test_process_runs(self):
        api.process_runs()
