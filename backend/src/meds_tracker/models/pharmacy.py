from sqlmodel import Field, SQLModel
from slugify import slugify
from . import UIDMixin


class InputPharmacy(SQLModel, table=False):
    name: str = Field(index=True)
    postcode: str = Field(index=True)
    address: str | None = Field(index=True, default=None)
    latitude: float | None = None
    longitude: float | None = None
    url: str | None = Field(default=None)


class Pharmacy(UIDMixin, InputPharmacy, table=True):
    pending_review: bool = Field(default=False, index=True, exclude=True)

    def make_uid(self):
        return slugify(f"{self.postcode}:{self.name}")
