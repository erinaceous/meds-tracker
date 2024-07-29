from sqlmodel import Field, SQLModel, UniqueConstraint
from uuid import UUID, uuid4
import datetime
import typing


class InputReport(SQLModel, table=False):
    medication_uid: str = Field(index=True)
    pharmacy_uid: str = Field(index=True)
    type: str | None = Field(index=True, default=None)
    dosage: str | None = Field(index=True, default=None)
    in_stock: bool = Field(index=True)
    reported_for_date: datetime.date = Field(
        default_factory=datetime.date.today, index=True
    )


class Report(InputReport, table=True):
    __table_args__ = (
        UniqueConstraint(
            "signature", "medication_uid", "pharmacy_uid", "dosage", "reported_for_date"
        ),
    )
    uuid: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    signature: str = Field(index=True, foreign_key="altcha.signature")
    pending_review: bool = Field(default=False, index=True)
    reported_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow, index=True
    )


class ReportError(SQLModel, table=False):
    details: str


class ReportOutput(SQLModel, table=False):
    report: Report | InputReport | None
    changed: bool = True
    error: ReportError | None = None


class ScoreReport(SQLModel, table=False):
    reported_for_date: datetime.date
    score: float = 0
    count_in_stock: int = 0
    count_out_of_stock: int = 0


class ScoreReports(SQLModel, table=False):
    medication_uid: str
    pharmacy_uid: str | None = None
    dosage: str | None = None
    scores: list[ScoreReport] = []
