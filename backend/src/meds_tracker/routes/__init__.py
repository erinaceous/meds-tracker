__all__ = ["altchas", "medications", "pharmacies", "reports", "static"]


SHORT_EXPIRY = 300  # 5 minutes
LONG_EXPIRY = 43200  # 12 hours


import importlib


for module in __all__:
    importlib.import_module(f".{module}", package=__name__)
