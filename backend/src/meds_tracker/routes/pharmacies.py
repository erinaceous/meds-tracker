from ..controllers.pharmacies import (
    locate_pharmacies,
    search_pharmacies,
    get_pharmacy_by_uid,
    create_pharmacy,
)
from ..persistent_db import depends as depends_persistent
from ..models.pharmacy import Pharmacy, InputPharmacy
from fastapi import Request, Query, Header, Response
from ..static_db import depends as depends_static
from ..libs.cache_header import cached_response
from ..api import app, limiter, cache
from sqlmodel import Session
from . import LONG_EXPIRY
import typing


@app.get("/pharmacies", tags=["Pharmacies"])
@limiter.limit("100/second")
# @cache(expire=LONG_EXPIRY)
async def list_pharmacies(
    request: Request,
    response: Response,
    latitude: float | None = None,
    longitude: float | None = None,
    radius: float | None = None,
    postcodes: typing.List[str] | None = Query(default=None),
    uids: typing.List[str] | None = Query(default=None),
    start_from: str | None = None,
    order: typing.Literal["asc", "desc"] = "asc",
    order_by: typing.Literal[
        "distance", "name", "postcode", "address", "uid"
    ] = "distance",
    session: Session = depends_static(),
) -> typing.List[Pharmacy]:
    return cached_response(
        await locate_pharmacies(
            session=session, latitude=latitude, longitude=longitude, radius=radius
        ),
        response,
        expire=LONG_EXPIRY,
    )


@app.post("/pharmacies", tags=["Pharmacies"])
@limiter.limit("100/second")
async def submit_pharmacy(
    request: Request,
    pharmacy: InputPharmacy,
    authorization: typing.Annotated[str | None, Header()] = None,
    persistent_session: Session = depends_persistent(),
    static_session: Session = depends_static(),
) -> Pharmacy:
    return await create_pharmacy(
        persistent_session=persistent_session,
        static_session=static_session,
        pharmacy=pharmacy,
        authorization=authorization,
    )


@app.get("/pharmacies/autocomplete/{search}", tags=["Pharmacies"])
@limiter.limit("100/second")
# @cache(expire=LONG_EXPIRY)
async def autocomplete_pharmacies(
    request: Request,
    response: Response,
    search: str,
    order: typing.Literal["asc", "desc"] = "asc",
    order_by: typing.Literal[
        "distance", "name", "postcode", "address", "uid"
    ] = "distance",
    session: Session = depends_static(),
) -> typing.List[Pharmacy]:
    return cached_response(
        await search_pharmacies(session=session, search=search),
        response,
        expire=LONG_EXPIRY,
    )


@app.get("/pharmacies/{uid}", tags=["Pharmacies"])
@limiter.limit("100/second")
# @cache(expire=LONG_EXPIRY)
async def get_medication(
    request: Request, response: Response, uid: str, session: Session = depends_static()
) -> Pharmacy:
    return cached_response(
        await get_pharmacy_by_uid(session, uid), response, expire=LONG_EXPIRY
    )
