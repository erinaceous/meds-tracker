from ..settings import settings, static_db_dir, static_db_path
from sqlmodel import SQLModel, Session, create_engine
from ..persistent_db import persistent_db
from fastapi import Depends
import os


if settings.static_db_uri == settings.persistent_db_uri:
    static_db = persistent_db
    from ..models import *
else:
    static_db = create_engine(settings.static_db_uri)


def init_static_db(recreate=False):
    if static_db_dir not in settings.static_db_uri:
        return
    os.makedirs(static_db_dir, exist_ok=True)
    if recreate is False and os.path.isfile(static_db_path):
        return
    # SQLModel.metadata.drop_all(static_db.engine)
    SQLModel.metadata.create_all(static_db.engine)


def session_context():
    return Session(static_db)


def yield_session():
    with session_context() as session:
        yield session


def depends():
    return Depends(yield_session)
