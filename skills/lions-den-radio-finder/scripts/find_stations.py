#!/usr/bin/env python3
"""Discover internet radio stations using Radio Browser's public search API.

No credentials or backend required. This script does not play or relay audio.
Radio Browser data is untrusted and provided without stream uptime guarantees.
"""
from __future__ import annotations

import argparse
import json
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

HOSTS = (
    "https://de1.api.radio-browser.info",
    "https://de2.api.radio-browser.info",
    "https://fi1.api.radio-browser.info",
)
SEARCH_FIELDS = {"name", "tag"}


def discover(query: str, field: str = "name", country: str = "", limit: int = 10) -> list[dict]:
    """Return up to limit distinct stations, failing over between public mirrors."""
    query = query.strip()
    if not query or len(query) > 120:
        raise ValueError("Query must be 1-120 characters.")
    if field not in SEARCH_FIELDS:
        raise ValueError("Search field must be 'name' or 'tag'.")
    if not 1 <= limit <= 20:
        raise ValueError("Limit must be between 1 and 20.")
    country = country.strip().upper()
    if country and (len(country) != 2 or not country.isalpha()):
        raise ValueError("Country must be a two-letter ISO country code.")

    params = {"hidebroken": "true", "order": "clickcount", "reverse": "true",
              "limit": str(min(60, limit * 3)), field: query}
    if country:
        params["countrycode"] = country
    if field == "tag":
        params["tagExact"] = "false"
    path = "/json/stations/search?" + urlencode(params)

    last_error: Exception | None = None
    for host in HOSTS:
        try:
            request = Request(host + path, headers={
                "Accept": "application/json",
                "User-Agent": "LionsDenRadioFinder/0.1 (public station search)",
            })
            with urlopen(request, timeout=8) as response:
                data = json.load(response)
            if not isinstance(data, list):
                raise ValueError("Directory response was not a list.")
            unique: list[dict] = []
            seen: set[str] = set()
            for item in data:
                if not isinstance(item, dict):
                    continue
                name = str(item.get("name") or "").strip()
                url = str(item.get("url_resolved") or item.get("url") or "").strip()
                if not name or urlsplit(url).scheme not in ("http", "https"):
                    continue
                ident = str(item.get("stationuuid") or name.casefold())
                if ident in seen:
                    continue
                seen.add(ident)
                unique.append({
                    "name": name[:160],
                    "country": str(item.get("country") or "")[:100],
                    "state": str(item.get("state") or "")[:100],
                    "codec": str(item.get("codec") or "")[:30],
                    "tags": str(item.get("tags") or "")[:200],
                    "stream_url": url,
                    "homepage": str(item.get("homepage") or "")[:300],
                    "station_id": str(item.get("stationuuid") or "")[:100],
                    "https_stream": urlsplit(url).scheme == "https",
                })
                if len(unique) >= limit:
                    break
            return unique
        except (HTTPError, URLError, OSError, TimeoutError, ValueError, json.JSONDecodeError) as error:
            last_error = error
    raise RuntimeError("All Radio Browser mirrors failed; try again later.") from last_error


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True, help="Name or genre to find")
    parser.add_argument("--field", choices=sorted(SEARCH_FIELDS), default="tag")
    parser.add_argument("--country", default="", help="Optional two-letter country code, e.g. JM")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()
    try:
        stations = discover(args.query, args.field, args.country, args.limit)
    except (ValueError, RuntimeError) as error:
        print(json.dumps({"error": str(error), "stations": []}), file=sys.stderr)
        return 1
    print(json.dumps({
        "source": "Radio Browser community directory",
        "query": args.query,
        "field": args.field,
        "stations": stations,
        "count": len(stations),
        "note": "Stream availability is not guaranteed. Browser playback requires a user gesture.",
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
