#!/usr/bin/env python3
import argparse
import requests
import json
import os
import re


ROOT="https://bnf.nice.org.uk/page-data/drugs"
CACHE_DIR=os.path.join(
    os.getcwd(),
    "download",
    "nice_bnf_drugs"
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--cache-dir", default=CACHE_DIR
    )
    parser.add_argument(
        "-r", "--api-root", default=ROOT
    )
    return parser.parse_args()


def request(page=None, root=ROOT, cache_dir=CACHE_DIR):
    cached_response = os.path.join(cache_dir, f"{page or 'index'}.json")
    if os.path.isfile(cached_response):
        with open(cached_response, "r") as fp:
            response_json = json.load(fp)
    else:
        url = f"{root}"
        if page is not None:
            url += f"/{page}"
        url += "/page-data.json"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        response_json = response.json()
        os.makedirs(
            os.path.dirname(cached_response),
            exist_ok=True
        )
        with open(cached_response, "w+") as fp:
            json.dump(response_json, fp, indent=1)
    result = response_json.get("result", {})
    data = result.get("data", {})
    return data


def get_index(root=ROOT, cache_dir=CACHE_DIR):
    data = request(root=root, cache_dir=cache_dir)
    allDrugs = data.get("allDrugs", {})
    letters = allDrugs.get("letters", {})
    for letter in letters:
        links = letter.get("links", [])
        for link in links:
            yield link.get("slug")


def get_meds_group(slug, cache_dir=CACHE_DIR, root=ROOT):
    data = request(root=root, page=slug, cache_dir=cache_dir)
    bnfDrug = data.get("bnfDrug", {})
    return bnfDrug


def get_products(meds_group):
    indicationsAndDose = meds_group.get("indicationsAndDose", {})
    if indicationsAndDose is None:
        return []
    prepContent = indicationsAndDose.get("prepContent", [])
    return prepContent


DOSAGE_REGEXES = {
    "micrograms": re.compile(r"(\d+(?:\.\d+)?[\-\s]*mi?c(?:ro)?g(?:rams)?)"),
    "mg": re.compile(r"(\d+(?:\.\d+)?[\-\s]*mg)")
}


def extract_dosages(product):
    # TODO: okay there is loads of human language to process in these fields,
    #  perhaps there is a data source where standard dosages of the products
    #  are listed..?
    #  eg Concerta XL is sold in 18, 27, 36, ..., 72 mg strengths
    doseEquivalence = product.get("doseEquivalence", None)
    if doseEquivalence is None:
        return None
    equivalences = set()
    for regex in DOSAGE_REGEXES.values():
        equivalences.update(
            regex.findall(doseEquivalence)
        )
    return equivalences


def get_medication_names():
    index = get_index()
    medications = {}
    for slug in index:
        meds_group = get_meds_group(slug)
        title = meds_group.get("title").strip()
        medications[title] = [
            product.get("contentFor").strip()
            for product in get_products(meds_group)
        ]
    return medications


def main():
    print(json.dumps(get_medication_names(), indent=1))


if __name__ == "__main__":
    main()
