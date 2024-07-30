from ..controllers.reports import create_or_update_reports, get_report_scores
from ..models.report import Report, InputReport, ReportOutput, ScoreReports
from fastapi import Request, Query, Header, Response, HTTPException
from ..persistent_db import depends as depends_persistent
from ..static_db import depends as depends_static
from ..libs.cache_header import cached_response
from ..api import app, limiter, cache
from sqlmodel import Session
from . import SHORT_EXPIRY
import asyncio
import typing


@app.get("/reports", tags=["Reports"])
@limiter.limit("100/second")
# @cache(expire=SHORT_EXPIRY)
async def get_reports(
    request: Request,
    response: Response,
    latitude: float | None = None,
    longitude: float | None = None,
    radius: float | None = None,
    max_age: float | None = 604800,
    medications: typing.List[str] | None = Query(default=None),
    pharmacies: typing.List[str] | None = Query(default=None),
    dosages: typing.List[str] | None = Query(default=None),
    types: typing.List[str] | None = Query(default=None),
    start_from: str | None = None,
    session: Session = depends_persistent(),
) -> typing.List[Report]:
    return cached_response([], response, expire=SHORT_EXPIRY)


@app.get("/reports/scores", tags=["Reports"])
@limiter.limit("100/second")
# @cache(expire=SHORT_EXPIRY)
async def get_scores(
    request: Request,
    response: Response,
    latitude: float | None = Query(default=None),
    longitude: float | None = Query(default=None),
    radius: float | None = Query(default=None),
    max_age: float | None = Query(default=604800),
    medication_uid: typing.List[str] | None = Query(default=None),
    pharmacy_uid: typing.List[str] | None = Query(default=None),
    dosage: typing.List[str] | None = Query(default=None),
    types: typing.List[str] | None = Query(default=None),
    include_pending: bool = Query(default=False),
    session: Session = depends_persistent(),
) -> typing.List[ScoreReports]:
    return cached_response(
        await get_report_scores(
            session,
            medication_uids=medication_uid,
            pharmacy_uids=pharmacy_uid,
            dosages=dosage,
            max_age=max_age,
            include_pending=include_pending,
        ),
        response,
        expire=SHORT_EXPIRY,
    )


@app.post("/reports", tags=["Reports"])
@limiter.limit("100/second")
async def submit_reports(
    request: Request,
    input_reports: typing.List[InputReport],
    authorization: typing.Annotated[str | None, Header()] = None,
    persistent_session: Session = depends_persistent(),
    static_session: Session = depends_static(),
) -> typing.List[ReportOutput]:
    await asyncio.sleep(1)
    return await create_or_update_reports(
        persistent_session, static_session, input_reports, authorization
    )
