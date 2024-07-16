from threading import local
import sqlite3
import os


_this_dir = os.path.dirname(__file__)
_default_db_path = os.path.join(_this_dir, "static.db")


class StaticDB:
    def __init__(
        self,
        path=_default_db_path
    ):
        src = sqlite3.connect(path)
        self.engine = sqlite3.connect(":memory:")
        src.backup(self.engine)
        src.close()

    def query(self, statement):
        return self.engine.cursor().execute(statement).fetchall()


local_ = local()


def instance():
    if not hasattr(local_, "static_db_instance"):
        local_.static_db_instance = StaticDB()
    return local_.static_db_instance
