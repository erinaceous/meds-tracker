#!/usr/bin/env python3
from src.meds_tracker.static_db import session_context, init_static_db, static_db
from sqlalchemy.dialects.postgresql import insert as postgresql_upsert
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert
from src.meds_tracker.models.medication import Medication
from src.meds_tracker.models.pharmacy import Pharmacy
from src.meds_tracker.settings import settings
import logging
import json
import os


upsert_funcs = {"sqlite": sqlite_upsert, "postgresql": postgresql_upsert}


def upsert(session, model, values, batch_size=100):
    for i in range(0, len(values), batch_size):
        statement = (
            upsert_funcs[session.get_bind().name](model)
            .values(values[i : i + batch_size])
            .on_conflict_do_nothing()
        )
        yield session.execute(statement)


def insert_pharmacies(pharmacies):
    pharmacies = [Pharmacy(**pharmacy).model_dump() for pharmacy in pharmacies]
    with session_context() as session:
        yield from upsert(session, Pharmacy, pharmacies)
        session.commit()


def meds_flat(medications):
    for category in medications.keys():
        yield Medication(category=category).model_dump()
        for product in medications.get(category, []):
            yield Medication(category=category, product=product).model_dump()


def insert_medications(medications):
    with session_context() as session:
        yield from upsert(session, Medication, list(meds_flat(medications)))
        session.commit()


def main():
    logging.basicConfig(level=logging.INFO)
    init_static_db(recreate=True)
    medications = json.load(
        open(
            os.path.abspath(
                os.path.join(settings.data_dir, "download", "medications.json")
            ),
            "r",
        )
    )
    for batch in insert_medications(medications):
        logging.info(
            "%s: Added medication categories: %s", settings.static_db_uri, batch
        )
    pharmacies = json.load(
        open(
            os.path.abspath(
                os.path.join(settings.data_dir, "download", "pharmacies.json")
            ),
            "r",
        )
    )
    for batch in insert_pharmacies(pharmacies):
        logging.info("%s: Added pharmacies: %s", settings.static_db_uri, batch)


if __name__ == "__main__":
    main()
