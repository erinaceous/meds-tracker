#!/usr/bin/env bash

this_dir="$(realpath "$(dirname "${0}")")" &&
code_dir="$(realpath "${this_dir}/..")" &&
data_dir="${PWD}/data" &&
echo "Getting postcodes" &&
${this_dir}/get_postcodes.py > "${data_dir}/download/postcodes.json" &&
echo "Getting pharmacies" &&
${this_dir}/get_pharmacies.py > "${data_dir}/download/pharmacies.json" &&
echo "Getting medications" &&
${this_dir}/get_medications.py > "${data_dir}/download/medications.json" &&
echo "Creating static DB" &&
python -m src.meds_tracker.static_db.create_static_db &&
echo "Making static DB files readonly" &&
chmod -w-x "${this_dir}/static.db" &&
echo "Generating metadata at ${code_dir}/static/metadata.json" &&
${this_dir}/output_metadata.py > "${code_dir}/static/metadata.json"