from .static_db import instance


def get_medications():
    return marshal(
        instance().query(
            "SELECT * FROM medications"
        )
    )


def search_medications(text):
    return marshal(
        instance().query(
            f"""
            SELECT * FROM medications
            WHERE
                category LIKE '%{text}%'
                OR product LIKE '%{text}%'
            """
        )
    )


def marshal(rows):
    return [
        {"category": row[0], "product": row[1]}
        for row in rows
    ]
