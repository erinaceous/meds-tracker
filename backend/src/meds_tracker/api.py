"""
UK crowd-sourced medication and pharmacy supply tracker: backend API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import __version__


app = FastAPI(
    version=__version__,
    title="UK medication tracker API",
    description=__doc__
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


from . import routes
