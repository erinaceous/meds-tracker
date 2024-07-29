from sqlmodel import Field
from uuid import uuid4


__all__ = ["altcha", "medication", "pharmacy", "report"]


class UIDMixin(object):
    uid: str = Field(primary_key=True, index=True)

    def make_uid(self) -> str:
        return uuid4().hex

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uid = self.make_uid()
