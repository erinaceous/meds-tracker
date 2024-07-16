#!/usr/bin/env bash

cd "$(dirname "${0}")" &&
echo "Getting postcodes" &&
./get_postcodes.py > ./download/postcodes.json &&
echo "Getting pharmacies" &&
./get_pharmacies.py > ./download/pharmacies.json &&
echo "Getting medications" &&
./get_medications.py > ./download/medications.json &&
echo "Creating static DB"
./create_static_db.py &&
echo "Compressing static DB" &&
gzip -9 -k download/static.db
echo "Moving files to $(realpath "${PWD}/../frontend/public/")"
cp -vf ./download/static.db ../backend/src/meds_tracker/database/
echo "Generating metadata"
./output_metadata.py > ../frontend/public/metadata.json