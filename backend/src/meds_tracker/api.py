"""
UK crowd-sourced pharmacy medication supply tracker backend API

https://github.com/erinaceous/meds-tracker
"""

from .settings import settings


init_sentry = False
if settings.sentry_dsn is not None and init_sentry is False:
    import sentry_sdk

    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=settings.sentry_traces_sample_rate,
        profiles_sample_rate=settings.sentry_profiles_sample_rate,
    )
    init_sentry = True


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from . import __version__
from .persistent_db import init_local_persistent_db
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from fastapi.middleware.gzip import GZipMiddleware
from msgpack_asgi import MessagePackMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    FastAPICache.init(InMemoryBackend())
    yield


init_local_persistent_db()
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    version=__version__,
    title="UK pharmacy supply tracker API",
    description=__doc__,
    lifespan=lifespan,
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=500)
app.add_middleware(MessagePackMiddleware)


from .routes import *
