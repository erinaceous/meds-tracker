from ..api import app
import typing


@app.get("/reports/area")
def get_reports(
    latitude: float,
    longitude: float,
    radius: float = 0,
    max_age: float = 604800,
    medications: typing.List[str] = None
):
    return {}


@app.get("/reports/pharmacy/{postcode}")
def get_reports(
    postcode: str,
    max_age: float = 604800,
    medications: typing.List[str] = None
):
    return {}


@app.get("/reports/medication/{name}")
def get_reports(
    medication: str,
    max_age: float = 604800
):
    return {}


@app.post("/reports/new")
def create_reports():
    return {}
