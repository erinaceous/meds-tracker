from ..models.report import (
    InputReport,
    Report,
    ReportError,
    ReportOutput,
    ScoreReport,
    ScoreReports,
)
from .medications import (
    get_known_dosages,
    get_known_types,
    get_medication_by_uid_static_or_persistent,
)
from .pharmacies import get_pharmacy_by_uid_static_or_persistent
from .altchas import get_altcha_from_header
from sqlmodel import Session, select
from fastapi import HTTPException
import sqlalchemy
import datetime
import typing


async def get_reports(
    session: Session, include_pending: bool = False
) -> typing.List[Report]:
    statement = select(Report)
    if include_pending is False:
        statement = statement.where(Report.pending_review == False)
    return session.exec(statement)


async def get_report_scores(
    session: Session,
    medication_uids: typing.List[str] | None = None,
    pharmacy_uids: typing.List[str] | None = None,
    dosages: typing.List[str] | None = None,
    max_age: float | None = None,
    include_pending: bool = False,
) -> typing.List[ScoreReports]:
    statement = (
        select(
            Report.medication_uid,
            Report.pharmacy_uid,
            Report.dosage,
            Report.reported_for_date,
            sqlalchemy.func.avg(Report.in_stock),
            sqlalchemy.func.count(Report.in_stock == True),
            sqlalchemy.func.count(Report.in_stock == False),
        )
        .group_by(
            Report.medication_uid,
            Report.pharmacy_uid,
            Report.dosage,
            Report.reported_for_date,
        )
        .order_by(
            Report.medication_uid.asc(),
            Report.dosage.asc(),
            Report.pharmacy_uid.asc(),
            Report.reported_for_date.asc(),
        )
    )
    if medication_uids is not None:
        statement = statement.filter(Report.medication_uid.in_(medication_uids))
    if pharmacy_uids is not None:
        statement = statement.filter(Report.pharmacy_uid.in_(pharmacy_uids))
    if dosages is not None:
        statement = statement.filter(Report.dosage.in_(dosages))
    if max_age is not None:
        statement = statement.filter(
            Report.reported_for_date
            >= datetime.datetime.now() - datetime.timedelta(seconds=max_age)
        )
    if include_pending is False:
        statement = statement.filter(Report.pending_review == False)
    reports = {}
    for row in session.exec(statement):
        key = (row[0], row[1], row[2])
        if key not in reports:
            reports[key] = ScoreReports(
                medication_uid=row[0], pharmacy_uid=row[1], dosage=row[2]
            )
        reports[key].scores.append(
            ScoreReport(
                reported_for_date=row[3],
                score=row[4],
                count_in_stock=row[5],
                count_out_of_stock=row[6],
            )
        )
    return reports.values()


async def find_existing_report(session: Session, report: InputReport) -> Report | None:
    statement = select(Report).filter(
        Report.signature == report.signature,
        Report.medication_uid == report.medication_uid,
        Report.pharmacy_uid == report.pharmacy_uid,
        Report.dosage == report.dosage,
        Report.reported_for_date == report.reported_for_date,
    )
    return session.exec(statement).one_or_none()


async def create_or_update_report(
    persistent_session: Session,
    static_session: Session,
    input_report: InputReport,
    signature: str,
) -> typing.Tuple[Report, bool]:
    report = Report(**input_report.dict(), signature=signature)
    medication = await get_medication_by_uid_static_or_persistent(
        static_session, persistent_session, report.medication_uid, raise_exception=True
    )
    pharmacy = await get_pharmacy_by_uid_static_or_persistent(
        static_session, persistent_session, report.pharmacy_uid, raise_exception=True
    )
    today = datetime.date.today()
    if report.reported_for_date > today:
        raise HTTPException(
            status_code=403, detail="Sorry! You can't make reports in the future."
        )
    pending_review = medication.pending_review or pharmacy.pending_review
    if report.type is not None:
        pending_review = pending_review or report.type not in await get_known_types(
            persistent_session, [report.medication_uid]
        )
    if report.dosage is not None:
        pending_review = pending_review or report.dosage not in await get_known_dosages(
            persistent_session, [report.medication_uid]
        )
    existing_report = await find_existing_report(persistent_session, report)
    if existing_report is not None:
        changed = False
        if (
            existing_report.in_stock != report.in_stock
            or existing_report.pending_review != pending_review
        ):
            if existing_report.reported_for_date < today:
                raise HTTPException(
                    status_code=403,
                    detail="Sorry! You can't edit a report older than today.",
                )
            existing_report.in_stock = report.in_stock
            existing_report.pending_review = pending_review
            changed = True
            persistent_session.commit()
        persistent_session.refresh(existing_report)
        return existing_report, changed
    report.pending_review = pending_review
    persistent_session.add(report)
    persistent_session.commit()
    persistent_session.refresh(report)
    return report, True


async def create_or_update_reports(
    persistent_session: Session,
    static_session: Session,
    reports: typing.List[InputReport],
    authorization: str,
) -> typing.List[ReportOutput]:
    altcha = await get_altcha_from_header(persistent_session, authorization)
    results = []
    for input_report in reports:
        result = ReportOutput(report=input_report)
        try:
            result.report, result.changed = await create_or_update_report(
                persistent_session, static_session, input_report, altcha.signature
            )
        except HTTPException as e:
            if e.status_code in [401, 403]:
                raise e
            result.error = ReportError(
                details=str(e),
            )
        results.append(result)
    return results
