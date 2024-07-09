#!/usr/bin/env python3
import argparse
import requests
import json
import os


ROOT = "https://opendata.nhsbsa.net"
START_PAGE = "/api/3/action/datastore_search?resource_id=CONSOL_PHARMACY_LIST_202324Q4&limit=100"
CACHE_DIR=os.path.join(
    os.getcwd(),
    "download",
    "pharmacies"
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--cache-dir", default=CACHE_DIR
    )
    return parser.parse_args()


def get_page(page, root=ROOT, cache_dir=CACHE_DIR):
    page_sane = page.replace("/", "_")
    cached_file = os.path.join(cache_dir, f"{page_sane}.json")
    if os.path.exists(cached_file):
        with open(cached_file, "r") as fp:
            response_json = json.load(fp)
    else:
        response = requests.get(f"{root}{page}", timeout=30)
        response.raise_for_status()
        response_json = response.json()
        os.makedirs(os.path.dirname(cached_file), exist_ok=True)
        with open(cached_file, "w+") as fp:
            json.dump(response_json, fp, indent=1)
    return response_json.get("result")


def get_pharmacies(page=None, offset=None, cache_dir=CACHE_DIR, root=ROOT):
    if page is None:
        page = START_PAGE
    if offset is not None:
        page += f"&offset={offset}"
    result = get_page(page=page, root=root, cache_dir=cache_dir)
    yield from result.get("records")
    if offset is None:
        for o in range(100, result.get("total"), 100):
            yield from get_pharmacies(
                page=page, cache_dir=cache_dir, root=root,
                offset=o
            )


def main():
    args = parse_args()
    for pharmacy in get_pharmacies(cache_dir=args.cache_dir):
        print(
            pharmacy.get("POST_CODE"),
            " ".join([
                pharmacy.get(f"ADDRESS_FIELD{x}", "") or ""
                for x in range(1, 5)
            ]).strip(),
            pharmacy.get("PHARMACY_TRADING_NAME"),
            sep=", "
        )


if __name__ == "__main__":
    main()
