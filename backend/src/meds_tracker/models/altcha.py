from functools import cached_property
from sqlmodel import Field, SQLModel
from pydantic import computed_field
import datetime
import enum


class Algorithm(enum.Enum):
    sha256 = "SHA-256"


class Altcha(SQLModel, table=True):
    algorithm: Algorithm = Algorithm.sha256
    challenge: str
    salt: str
    number: int | None = None
    signature: str = Field(primary_key=True, index=True)
    expires: datetime.datetime | None = Field(default=None, index=True)
    verified: bool = False

    @computed_field
    @cached_property
    def active(self) -> bool:
        if self.verified is False:
            return False
        now = datetime.datetime.now()
        return now < self.expires


class AltchaPayload(SQLModel, table=False):
    payload: str
