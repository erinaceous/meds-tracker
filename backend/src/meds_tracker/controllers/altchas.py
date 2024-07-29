from ..models.altcha import Altcha, Algorithm
from sqlmodel import Session, select
from fastapi import HTTPException
from ..settings import settings
import datetime
import hashlib
import random
import hmac
import math
import os


def create_hash(salt: str, number: float) -> str:
    hasher = hashlib.sha256()
    hasher.update((salt + str(number)).encode("utf-8"))
    hash_value = hasher.digest()
    return hash_value.hex()


def create_hmac(secret_key: str, challenge: str) -> str:
    hash_algorithm = "sha256"
    hmac_object = hmac.new(
        secret_key.encode(), challenge.encode(), getattr(hashlib, hash_algorithm)
    )
    return hmac_object.hexdigest()


def generate_challenge() -> Altcha:
    now = datetime.datetime.now(datetime.UTC)
    tomorrow = now + datetime.timedelta(days=1)
    tomorrow = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    salt = f"{os.urandom(32).hex()}?expires={int(math.floor(tomorrow.timestamp()))}"
    secret_number = random.randrange(10000, 100000, 1)
    challenge = create_hash(salt, secret_number)
    signature = create_hmac(settings.hmac_secret, challenge)
    return Altcha(
        algorithm=Algorithm.sha256,
        challenge=challenge,
        salt=salt,
        signature=signature,
        verified=False,
        expires=tomorrow,
    )


def verify(altcha: Altcha, raise_exception: bool = True) -> bool:
    alg_okay = altcha.algorithm == Algorithm.sha256
    if alg_okay is False:
        if raise_exception:
            raise HTTPException(
                status_code=400, detail=f"Invalid algorithm '{altcha.algorithm}'"
            )
        return False
    challenge_okay = altcha.challenge == create_hash(altcha.salt, altcha.number)
    if challenge_okay is False:
        if raise_exception:
            raise HTTPException(status_code=400, detail="Invalid challenge")
        return False
    signature_okay = altcha.signature == create_hmac(
        settings.hmac_secret, altcha.challenge
    )
    if signature_okay is False:
        if raise_exception:
            raise HTTPException(status_code=400, detail="Invalid signature")
        return False
    if alg_okay and challenge_okay and signature_okay:
        return True
    if raise_exception:
        raise HTTPException(status_code=400)
    return False


async def get_altcha_by_signature(
    session: Session, signature: str, raise_exception: bool = True
) -> Altcha:
    statement = select(Altcha).where(Altcha.signature == signature)
    altcha = session.exec(statement).one_or_none()
    if altcha is None and raise_exception:
        raise HTTPException(
            status_code=401, detail=f"No record of signature '{signature}'"
        )
    return altcha


async def verify_and_update(
    session: Session, altcha: Altcha, raise_exception: bool = True
) -> Altcha:
    existing_altcha = await get_altcha_by_signature(
        session, altcha.signature, raise_exception=False
    )
    if existing_altcha and raise_exception:
        raise HTTPException(
            status_code=409,
            detail=f"Altcha with signature '{altcha.signature}' already exists",
        )
    if "?expires" in altcha.salt:
        expires = math.ceil(float(altcha.salt.split("?expires=")[1]))
        altcha.expires = datetime.datetime.fromtimestamp(expires, datetime.UTC)
    now = datetime.datetime.now(datetime.UTC)
    tomorrow = now + datetime.timedelta(days=1)
    tomorrow = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    if altcha.expires is None or tomorrow < altcha.expires:
        raise HTTPException(status_code=400, detail="Invalid altcha expiration time")
    altcha.verified = verify(altcha, raise_exception=raise_exception)
    session.add(altcha)
    session.commit()
    session.refresh(altcha)
    return altcha


async def get_altcha_from_header(
    session: Session, authorization: str, raise_inactive: bool = True
) -> Altcha:
    if "Bearer " not in authorization:
        raise HTTPException(
            status_code=400,
            detail="Invalid Authorization header: Must be a bearer token",
        )
    signature = authorization.split(" ")[1]
    altcha = await get_altcha_by_signature(session, signature)
    if raise_inactive is True and altcha.active is False:
        raise HTTPException(
            status_code=401,
            detail="Signature no longer valid, please re-authenticate with a new altcha challenge",
        )
    return altcha
