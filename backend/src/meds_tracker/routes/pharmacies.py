from ..database.pharmacies import locate_pharmacies, search_pharmacies
from ..api import app
import typing


@app.get("/pharmacies/location")
def list_pharmacies(
    latitude: float = None,
    longitude: float = None,
    radius: float = None
):
    return locate_pharmacies(
        latitude=latitude,
        longitude=longitude,
        radius=radius
    )


@app.get("/pharmacies/autocomplete/{postcode}")
def autocomplete_pharmacies(postcode: str):
    return search_pharmacies(postcode=postcode)
