import json
import unittest
from smb3_leaderboards import main


class TestMain(unittest.TestCase):
    def test_logic(self):
        self.assertEqual("Hello World!", main.logic())