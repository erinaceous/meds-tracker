#!/usr/bin/env python3
from get_pharmacies import get_pharmacies
import json
import os


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


def main():
    postcodes = parse_postcode_csv()
    for pharmacy in get_pharmacies():
        postcode = pharmacy.get("POST_CODE").strip()
        postcode_normalised = postcode.replace(" ", "").strip().lower()
        pharmacy.update(**postcodes.get(postcode_normalised, {
            "LATITUDE": None, "LONGITUDE": None
        }))
        print(json.dumps({
            "name": pharmacy.get("PHARMACY_TRADING_NAME"),
            "address": "\n".join([
                pharmacy.get(f"ADDRESS_FIELD{x}", "") or ""
                for x in range(1, 5)
            ]).strip(),
            "postcode": postcode,
            "latitude": pharmacy.get("LATITUDE"),
            "longitude": pharmacy.get("LONGITUDE"),
        }))


if __name__ == "__main__":
    main()
