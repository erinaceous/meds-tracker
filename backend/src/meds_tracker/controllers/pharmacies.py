from ..models.pharmacy import Pharmacy, InputPharmacy
from .altchas import get_altcha_from_header
from sqlmodel import Session, select
from ..libs.geo import boundingBox
from fastapi import HTTPException
import sqlalchemy
import typing


ONE_METRE_MILES = 0.0006213712
ONE_METRE_KM = 0.001
ONE_MILE_KM = 1.609344


async def locate_pharmacies(
    session: Session,
    latitude: float,
    longitude: float,
    radius: float = 0,
    include_pending: bool = False,
) -> typing.List[Pharmacy]:
    # FIXME: calculate the bounding box properly.  You can't just subtract
    #   metres from degrees latitude/longitude - distance in degrees varies
    #   as latitude changes.
    radius *= ONE_MILE_KM
    radius = max(ONE_METRE_KM, radius)
    min_lat, min_lon, max_lat, max_lon = boundingBox(latitude, longitude, radius)
    statement = select(Pharmacy).where(
        sqlalchemy.and_(
            sqlalchemy.and_(Pharmacy.latitude >= min_lat, Pharmacy.latitude <= max_lat),
            sqlalchemy.and_(
                Pharmacy.longitude >= min_lon, Pharmacy.longitude <= max_lon
            ),
        )
    )
    if include_pending is False:
        statement = statement.where(Pharmacy.pending_review == False)
    return session.exec(statement)


async def search_pharmacies(
    session: Session, search: str, include_pending: bool = False
) -> typing.List[Pharmacy]:
    search = search.strip().lower().replace(" ", "%")
    statement = (
        select(Pharmacy)
        .filter(
            sqlalchemy.or_(
                sqlalchemy.func.lower(
                    sqlalchemy.func.replace(Pharmacy.postcode, " ", "").ilike(
                        f"%{search}%"
                    )
                ),
                sqlalchemy.func.lower(Pharmacy.address).ilike(f"%{search}%"),
                sqlalchemy.func.lower(Pharmacy.name).ilike(f"%{search}%"),
            )
        )
        .order_by(
            sqlalchemy.func.instr(
                sqlalchemy.func.lower(
                    sqlalchemy.func.replace(Pharmacy.postcode, " ", "")
                ),
                search,
            ).asc(),
            sqlalchemy.func.instr(
                sqlalchemy.func.lower(Pharmacy.address), search
            ).asc(),
            sqlalchemy.func.instr(sqlalchemy.func.lower(Pharmacy.name), search).asc(),
        )
    )
    if include_pending is False:
        statement = statement.filter(Pharmacy.pending_review == False)
    statement = statement.limit(50)
    return session.exec(statement)


async def get_pharmacy_by_uid(
    session: Session, uid: str, raise_exception: bool = True
) -> Pharmacy:
    statement = select(Pharmacy).filter(Pharmacy.uid == uid)
    pharmacy = session.exec(statement).one_or_none()
    if pharmacy is None and raise_exception is True:
        raise HTTPException(
            status_code=404, detail=f"Pharmacy with uid '{uid}' not found"
        )
    return pharmacy


async def get_pharmacy_by_uid_static_or_persistent(
    static_session: Session,
    persistent_session: Session,
    uid: str,
    raise_exception: bool = True,
) -> Pharmacy:
    pharmacy = await get_pharmacy_by_uid(static_session, uid, raise_exception=False)
    if pharmacy is not None:
        return pharmacy
    return await get_pharmacy_by_uid(
        persistent_session, uid, raise_exception=raise_exception
    )


async def create_pharmacy(
    persistent_session: Session,
    static_session: Session,
    pharmacy: InputPharmacy,
    authorization: str,
) -> Pharmacy:
    await get_altcha_from_header(persistent_session, authorization)
    pharmacy = Pharmacy(**pharmacy.model_dump(), pending_review=True)
    existing_pharmacy = await get_pharmacy_by_uid_static_or_persistent(
        static_session, persistent_session, pharmacy.uid, raise_exception=False
    )
    if existing_pharmacy is not None:
        return existing_pharmacy
    persistent_session.flush()
    persistent_session.add(pharmacy)
    persistent_session.commit()
    persistent_session.refresh(pharmacy)
    return pharmacy
