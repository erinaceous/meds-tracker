#!/usr/bin/env bash

curl 'https://www.getthedata.com/downloads/open_postcode_geo.csv.tar.gz' \
  | tar -z --extract --one-top-level="${PWD}/download" open_postcode_geo.csv
