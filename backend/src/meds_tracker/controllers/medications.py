from ..models.medication import Medication, InputMedication
from .altchas import get_altcha_from_header
from sqlmodel import Session, select
from ..models.report import Report
from fastapi import HTTPException
from . import RE_WHITESPACE
import sqlalchemy
import typing


async def get_medications(
    session: Session, include_pending: bool = False
) -> typing.List[Medication]:
    statement = select(Medication)
    if include_pending is False:
        statement = statement.filter(Medication.pending_review == False)
    return session.exec(statement)


async def get_medication_categories(
    session: Session, include_pending: bool = False
) -> typing.List[str]:
    statement = select(Medication.category).distinct()
    if include_pending is False:
        statement = statement.filter(Medication.pending_review == False)
    return session.exec(statement)


async def search_medications(
    session: Session, text: str, include_pending: bool = False
) -> typing.List[Medication]:
    text = text.lower().strip()
    search = RE_WHITESPACE.sub("%", text)
    statement = (
        select(Medication)
        .filter(
            sqlalchemy.or_(
                sqlalchemy.func.lower(Medication.category).ilike(f"%{search}%"),
                sqlalchemy.func.lower(Medication.product).ilike(f"%{search}%"),
                sqlalchemy.func.lower(Medication.uid).ilike(f"%{search}%"),
            )
        )
        .order_by(
            sqlalchemy.nullslast(
                sqlalchemy.func.instr(
                    sqlalchemy.func.lower(Medication.product),
                    text,
                ).asc()
            ),
            sqlalchemy.func.instr(
                sqlalchemy.func.lower(Medication.category), text
            ).asc(),
            sqlalchemy.nullslast(Medication.product.asc()),
            Medication.category.asc(),
        )
    )
    if include_pending is False:
        statement = statement.filter(Medication.pending_review == False)
    statement = statement.limit(100)
    return session.exec(statement)


async def get_medication_by_uid(
    session: Session, uid: str, raise_exception: bool = True
) -> Medication:
    statement = select(Medication).filter(Medication.uid == uid)
    medication = session.exec(statement).one_or_none()
    if medication is None and raise_exception is True:
        raise HTTPException(
            status_code=404, detail=f"Medication with uid '{uid}' not found"
        )
    return medication


async def get_medication_by_uid_static_or_persistent(
    static_session: Session,
    persistent_session: Session,
    uid: str,
    raise_exception: bool = True,
) -> Medication:
    medication = await get_medication_by_uid(static_session, uid, raise_exception=False)
    if medication is not None:
        return medication
    return await get_medication_by_uid(
        persistent_session, uid, raise_exception=raise_exception
    )


async def get_known_dosages(
    session: Session, medication_uids: typing.List[str]
) -> typing.List[str | None]:
    statement = (
        select(Report.dosage)
        .distinct(Report.dosage)
        .filter(
            Report.pending_review == False, Report.medication_uid.in_(medication_uids)
        )
        .order_by(Report.dosage.asc())
    )
    return session.exec(statement)


async def get_known_types(
    session: Session, medication_uids: typing.List[str]
) -> typing.List[str | None]:
    statement = (
        select(Report.type)
        .distinct(Report.type)
        .filter(
            Report.pending_review == False, Report.medication_uid.in_(medication_uids)
        )
        .order_by(Report.type.asc())
    )
    return session.exec(statement)


async def create_medication(
    persistent_session: Session,
    static_session: Session,
    medication: InputMedication,
    authorization: str,
) -> Medication:
    await get_altcha_from_header(persistent_session, authorization)
    medication = Medication(**medication.model_dump(), pending_review=True)
    existing_medication = await get_medication_by_uid_static_or_persistent(
        persistent_session, static_session, medication.uid, raise_exception=False
    )
    if existing_medication:
        return existing_medication
    persistent_session.flush()
    persistent_session.add(medication)
    persistent_session.commit()
    persistent_session.refresh(medication)
    return medication
