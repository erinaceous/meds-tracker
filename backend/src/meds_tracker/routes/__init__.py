__all__ = [
    "medications",
    "pharmacies",
    "reports"
]


import importlib


for module in __all__:
    importlib.import_module(f".{module}", package=__name__)
