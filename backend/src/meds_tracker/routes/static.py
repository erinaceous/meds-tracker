from fastapi.staticfiles import StaticFiles
from ..api import app
import os


this_dir = os.path.dirname(__file__)
static_dir = os.path.abspath(os.path.join(this_dir, "..", "static"))


app.mount("/static", StaticFiles(directory=static_dir), name="static")
