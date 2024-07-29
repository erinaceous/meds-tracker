from pydantic_settings import BaseSettings, SettingsConfigDict
import pathlib
import uuid
import os


this_dir = os.path.dirname(os.path.abspath(__file__))

static_db_dir = os.path.realpath(os.path.join(this_dir, "static_db"))
static_db_path = os.path.join(static_db_dir, "static.db")

data_dir = os.path.join(os.getcwd(), "data")
persistent_db_path = os.path.join(data_dir, "persistent.db")

# static_db_dir = data_dir
# static_db_path = persistent_db_path


class Settings(BaseSettings):
    static_db_dir: pathlib.Path = static_db_dir
    data_dir: pathlib.Path = data_dir

    static_db_uri: str | None = f"sqlite:///{static_db_path}"
    persistent_db_uri: str | None = f"sqlite:///{persistent_db_path}"

    # NOTE the default HMAC key will be different each time the *process* is
    # started up.  This might make a difference wrt scaling the workload - not
    # sure.
    hmac_secret: str | None = uuid.uuid4().hex

    sentry_dsn: str | None = None
    sentry_traces_sample_rate: float = 0.1
    sentry_profiles_sample_rate: float = 0.1

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
