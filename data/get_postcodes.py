#!/usr/bin/env python3
import argparse
import requests
import tempfile
import tarfile
import json
import io
import os


URL = "https://www.getthedata.com/downloads/open_postcode_geo.csv.tar.gz"


def parse_postcode_csv():
    postcodes_path = os.path.join(
        os.getcwd(),
        "download",
        "open_postcode_geo.csv"
    )
    postcodes = {}
    with open(postcodes_path, "r") as fp:
        for line in fp:
            if "terminated" in line:
                continue
            (
                postcode, status, usertype, easting, northing,
                positional_quality_indicator, country, latitude, longitude,
                postcode_no_space, postcode_fixed_width_seven,
                postcode_fixed_width_eight, postcode_area, postcode_district,
                postcode_sector, outcode, incode
            ) = line.strip().split(",")
            if "\\N" in latitude or "\\N" in longitude:
                continue
            latitude, longitude = float(latitude), float(longitude)
            postcode_normalised = postcode.replace(" ", "").strip().lower()
            postcodes[postcode_normalised] = {
                "LATITUDE": latitude, "LONGITUDE": longitude
            }
    return postcodes


def fetch_archive():
    response = requests.get(URL, stream=True)
    response.raise_for_status()
    return response


def streamed_read_csv():
    with tempfile.TemporaryFile("w+b") as tmp_fd:
        with fetch_archive() as download:
            tmp_fd.write(download.content)
        tmp_fd.seek(0)
        with tarfile.open(fileobj=tmp_fd, mode="r:gz") as tar:
            file = tar.extractfile("open_postcode_geo.csv")
            lines = io.TextIOWrapper(file, encoding="utf-8")
            for line in lines:
                if "terminated" in line or "\\N" in line:
                    continue
                row = line.strip().split(",")
                yield [row[0], float(row[7]), float(row[8])]


def main():
    print(
        json.dumps(
            list(streamed_read_csv()),
            indent=1
        )
    )


if __name__ == "__main__":
    main()
