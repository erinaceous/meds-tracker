from ..controllers.medications import (
    get_medications,
    get_medication_categories,
    search_medications,
    get_medication_by_uid,
    get_medication_by_uid_static_or_persistent,
    create_medication,
    get_known_dosages,
    get_known_types,
)
from ..models.medication import Medication, InputMedication
from ..persistent_db import depends as depends_persistent
from fastapi import Request, Query, Header, Response
from ..static_db import depends as depends_static
from ..libs.cache_header import cached_response
from ..api import app, limiter, cache
from sqlmodel import Session
from . import LONG_EXPIRY
import typing


@app.get("/medications", tags=["Medications"])
@limiter.limit("100/second")
# @cache(expire=LONG_EXPIRY)
async def list_medications(
    request: Request,
    response: Response,
    session: Session = depends_static(),
    categories: typing.List[str] | None = Query(default=None),
    products: typing.List[str] | None = Query(default=None),
    uids: typing.List[str] | None = Query(default=None),
    start_from: str | None = None,
    order: typing.Literal["asc", "desc"] = "asc",
    order_by: typing.Literal["product", "category", "uid"] = "product",
) -> typing.List[Medication]:
    return cached_response(await get_medications(session), response, expire=LONG_EXPIRY)


@app.post("/medications", tags=["Medications"])
@limiter.limit("100/second")
async def submit_medication(
    request: Request,
    medication: InputMedication,
    authorization: typing.Annotated[str | None, Header()] = None,
    persistent_session: Session = depends_persistent(),
    static_session: Session = depends_static(),
):
    return await create_medication(
        persistent_session, static_session, medication, authorization
    )


@app.get("/medications/categories", tags=["Medications"])
@limiter.limit("100/second")
# @cache(expire=LONG_EXPIRY)
async def list_medication_categories(
    request: Request,
    response: Response,
    session: Session = depends_static(),
) -> typing.List[str]:
    return cached_response(
        await get_medication_categories(session), response, expire=LONG_EXPIRY
    )


@app.get("/medications/autocomplete/{text}", tags=["Medications"])
@limiter.limit("100/second")
# @cache(expire=LONG_EXPIRY)
async def autocomplete_medications(
    request: Request,
    response: Response,
    text: str,
    order: typing.Literal["asc", "desc"] = "asc",
    order_by: typing.Literal["product", "category", "uid"] = "product",
    session: Session = depends_static(),
) -> typing.List[Medication]:
    return cached_response(
        await search_medications(session, text), response, expire=LONG_EXPIRY
    )


@app.get("/medications/dosages", tags=["Medications"])
@limiter.limit("100/second")
# @cache(expire=LONG_EXPIRY)
async def get_medication_dosages(
    request: Request,
    response: Response,
    uid: typing.List[str] = Query(),
    session: Session = depends_persistent(),
) -> typing.List[str | None]:
    return cached_response(
        await get_known_dosages(session, uid), response, expire=LONG_EXPIRY
    )


@app.get("/medications/types", tags=["Medications"])
@limiter.limit("100/second")
# @cache(expire=LONG_EXPIRY)
async def get_medication_types(
    request: Request,
    response: Response,
    uid: typing.List[str] = Query(),
    session: Session = depends_persistent(),
) -> typing.List[str | None]:
    return cached_response(
        await get_known_types(session, uid), response, expire=LONG_EXPIRY
    )


@app.get("/medications/{uid}", tags=["Medications"])
@limiter.limit("100/second")
# @cache(expire=LONG_EXPIRY)
async def get_medication(
    request: Request,
    response: Response,
    uid: str,
    static_session: Session = depends_static(),
    persistent_session: Session = depends_persistent(),
) -> Medication:
    return cached_response(
        await get_medication_by_uid_static_or_persistent(
            static_session, persistent_session, uid
        ),
        response,
        expire=LONG_EXPIRY,
    )
