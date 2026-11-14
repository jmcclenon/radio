"""Offline tests for Lion's Den Radio Finder (no external network required)."""
import io
import importlib.util
import pathlib
import unittest
from unittest.mock import patch

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "skills" / "lions-den-radio-finder" / "scripts" / "find_stations.py"
spec = importlib.util.spec_from_file_location("find_stations", SCRIPT)
finder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(finder)


class RadioSearchTests(unittest.TestCase):
    def test_request_parsing_and_deduplication(self):
        payload = b'[{"name":"Roots FM","stationuuid":"abc","country":"Jamaica","url_resolved":"https://example.com/radio.mp3","tags":"reggae"},' \
                  b'{"name":"Roots FM duplicate","stationuuid":"abc","url":"https://example.com/dup.mp3"},' \
                  b'{"name":"Invalid Stream","stationuuid":"invalid","url":"javascript:alert(1)"},' \
                  b'{"name":"Jazz","stationuuid":"def","url":"http://example.com/jazz.mp3"}]'
        with patch.object(finder, "urlopen", return_value=io.BytesIO(payload)) as remote:
            result = finder.discover("roots", field="tag", country="jm", limit=5)
        self.assertEqual([x["name"] for x in result], ["Roots FM", "Jazz"])
        self.assertTrue(result[0]["https_stream"])
        self.assertFalse(result[1]["https_stream"])
        req = remote.call_args.args[0]
        self.assertIn("countrycode=JM", req.full_url)
        self.assertIn("tag=roots", req.full_url)

    def test_mirror_failover(self):
        def fake_open(request, timeout=8):
            if "de1." in request.full_url:
                raise finder.URLError("temporary failure")
            return io.BytesIO(b'[{"name":"A","url":"https://example.com/live"}]')
        with patch.object(finder, "urlopen", side_effect=fake_open) as remote:
            result = finder.discover("jazz")
        self.assertEqual(result[0]["name"], "A")
        self.assertEqual(remote.call_count, 2)

    def test_invalid_arguments(self):
        cases = [
            {"query": ""}, {"query": "x" * 121},
            {"query": "jazz", "country": "United States"},
            {"query": "jazz", "limit": 0},
            {"query": "jazz", "field": "unsupported"},
        ]
        for params in cases:
            with self.subTest(params=params), self.assertRaises(ValueError):
                finder.discover(**params)

    def test_empty_response(self):
        with patch.object(finder, "urlopen", return_value=io.BytesIO(b'[]')):
            self.assertEqual(finder.discover("unknown"), [])


if __name__ == "__main__":
    unittest.main()
