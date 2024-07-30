from ..controllers.altchas import (
    generate_challenge,
    verify_and_update,
    get_altcha_from_header,
)
from ..models.altcha import Altcha, AltchaPayload
from fastapi import Request, Response, Header
from pydantic_core import from_json
from ..persistent_db import depends
from ..api import app, limiter
from sqlmodel import Session
import asyncio
import base64
import typing


@app.get("/altcha/challenge", tags=["Registration"])
@limiter.limit("100/second")
async def altcha_challenge(
    request: Request,
) -> Altcha:
    await asyncio.sleep(3)
    return generate_challenge()


@app.post("/altcha/verify", tags=["Registration"])
@limiter.limit("100/second")
async def altcha_validate(
    request: Request,
    response: Response,
    data: AltchaPayload,
    session: Session = depends(),
) -> Altcha:
    await asyncio.sleep(1)
    altcha = Altcha.parse_obj(from_json(base64.b64decode(data.payload)))
    altcha = await verify_and_update(session, altcha, raise_exception=True)
    return altcha


@app.get("/altcha", tags=["Registration"])
@limiter.limit("100/second")
async def altcha_check(
    request: Request,
    response: Response,
    authorization: typing.Annotated[str | None, Header()] = None,
    session: Session = depends(),
) -> Response:
    await asyncio.sleep(1)
    await get_altcha_from_header(session, authorization)
    response.status_code = 204
    return response
