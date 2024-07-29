from .settings import settings, data_dir, persistent_db_path
from sqlmodel import SQLModel, Session, create_engine
from fastapi import Depends
import os


persistent_db = create_engine(settings.persistent_db_uri)


def init_local_persistent_db(recreate=False):
    if data_dir not in settings.persistent_db_uri:
        return
    os.makedirs(data_dir, exist_ok=True)
    if recreate is False and os.path.isfile(persistent_db_path):
        return
    # SQLModel.metadata.drop_all(persistent_db.engine)
    from .models.altcha import Altcha
    from .models.report import Report
    from .models.pharmacy import Pharmacy
    from .models.medication import Medication

    SQLModel.metadata.create_all(persistent_db.engine)


def session_context():
    return Session(persistent_db)


def yield_session():
    with session_context() as session:
        yield session


def depends():
    return Depends(yield_session)
