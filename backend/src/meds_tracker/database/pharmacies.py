from ..libs.geo import boundingBox
from .static_db import instance


ONE_METRE_MILES = 0.0006213712
ONE_METRE_KM = 0.001
ONE_MILE_KM = 1.609344


def locate_pharmacies(
    latitude: float, longitude: float, radius: float = 0
):
    # FIXME: calculate the bounding box properly.  You can't just subtract
    #   metres from degrees latitude/longitude - distance in degrees varies
    #   as latitude changes.
    radius *= ONE_MILE_KM
    radius = max(ONE_METRE_KM, radius)
    min_lat, min_lon, max_lat, max_lon = boundingBox(
        latitude, longitude, radius
    )
    return marshal(
        instance().query(
            f"""
            SELECT * FROM pharmacies
            WHERE
               (latitude >= {min_lat} and latitude <= {max_lat})
               AND (longitude >= {min_lon} and longitude <= {max_lon})
            """
        )
    )


def search_pharmacies(postcode: str):
    postcode = postcode.strip().upper()
    return marshal(
        instance().query(
            f"""
            SELECT * FROM pharmacies
            WHERE postcode LIKE '{postcode}%'
            """
        )
    )


def marshal(rows):
    return [
        {
            "name": row[0],
            "postcode": row[1],
            "address": row[2],
            "latitude": row[3],
            "longitude": row[4]
        }
        for row in rows
    ]
