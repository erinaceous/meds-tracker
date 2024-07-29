from fastapi import Response
from functools import wraps


def cache(expire=3600):
    def decorator(func):
        @wraps(func)
        def wrapper(response: Response, *args, **kwargs):
            response.headers["Cache-Control"] = "public, max-age={}".format(expire)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def cached_response(output, response: Response, expire=3600):
    response.headers["Cache-Control"] = "public, max-age={}".format(expire)
    return output
