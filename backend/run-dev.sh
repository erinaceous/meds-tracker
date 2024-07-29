#!/usr/bin/env bash
source venv/bin/activate
pip install -r requirements.txt
source .env
fastapi dev src/meds_tracker/api.py