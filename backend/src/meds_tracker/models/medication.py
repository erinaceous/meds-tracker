from sqlmodel import Field, SQLModel
from slugify import slugify
from . import UIDMixin


class InputMedication(SQLModel, table=False):
    category: str = Field(index=True)
    product: str | None = Field(default=None, index=True)
    url: str | None = Field(default=None)


class Medication(UIDMixin, InputMedication, table=True):
    pending_review: bool = Field(default=False, index=True, exclude=True)

    def make_uid(self) -> str:
        name = slugify(self.category)
        if self.product is not None:
            name += f":{slugify(self.product)}"
        return name
