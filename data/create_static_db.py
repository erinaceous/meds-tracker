#!/usr/bin/env python3
import sqlite3
import glob
import json
import os


THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.abspath(
    os.path.join(
        THIS_DIR,
        "download",
        "static.db"
    )
)
SCRIPTS = glob.glob(
    os.path.join(
        os.path.abspath(
            os.path.join(
                THIS_DIR,
                "static_db"
            )
        ),
        "*.sql"
    )
)


def connect_database():
    return sqlite3.connect(DB_PATH)


def init_database(db):
    cur = db.cursor()
    for script_path in SCRIPTS:
        script = open(script_path, "r").read()
        cur.executescript(script)
    db.commit()


def create_database():
    if os.path.isfile(DB_PATH):
        os.unlink(DB_PATH)
    db = connect_database()
    init_database(db)
    return db


def insert_postcodes(db, postcodes):
    cur = db.cursor()
    cur.executemany(
        """
        INSERT INTO postcodes VALUES (?, ?, ?)
        """,
        postcodes
    )
    db.commit()


def insert_pharmacies(db, pharmacies):
    cur = db.cursor()
    cur.executemany(
        """
        INSERT INTO pharmacies VALUES (?, ?, ?, ?, ?)
        """,
        [
            [
                pharmacy.get("name"),
                pharmacy.get("postcode"),
                pharmacy.get("address"),
                pharmacy.get("latitude"),
                pharmacy.get("longitude")
            ]
            for pharmacy in pharmacies
        ]
    )
    db.commit()


def insert_medications(db, medications):
    cur = db.cursor()
    flat = []
    for category in medications.keys():
        flat.append([category, None])
        for product in medications.get(category, []):
            flat.append([category, product])
    cur.executemany(
        """
        INSERT INTO medications VALUES (?, ?)
        """,
        flat
    )
    db.commit()


def finish(db):
    cur = db.cursor()
    cur.execute("""VACUUM;""")
    db.commit()


def main():
    db = create_database()
    #postcodes = json.load(open(os.path.abspath(os.path.join(THIS_DIR, "download", "postcodes.json")), "r"))
    #insert_postcodes(db, postcodes)
    pharmacies = json.load(open(os.path.abspath(os.path.join(THIS_DIR, "download", "pharmacies.json")), "r"))
    insert_pharmacies(db, pharmacies)
    medications = json.load(open(os.path.abspath(os.path.join(THIS_DIR, "download", "medications.json")), "r"))
    insert_medications(db, medications)
    finish(db)


if __name__ == "__main__":
    main()
