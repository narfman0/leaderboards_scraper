import json
import unittest
from smb3_leaderboards import src_ajax


class TestSrcAjax(unittest.TestCase):
    def test_store_category_runs(self):
        with open("tests/fixtures/smb3WarplessAjax1.html") as file:
            src_ajax.store_category_runs("abc123", file.read())