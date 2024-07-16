from ..database.medications import get_medications, search_medications
from ..api import app
import typing


@app.get("/medications")
def list_medications(
    categories: typing.List[str] = None,
    products: typing.List[str] = None,
):
    return get_medications()


@app.get("/medications/autocomplete/{text}")
def autocomplete_medications(text: str):
    return search_medications(text)
