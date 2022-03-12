def normalize_path_params( city = None, stars_min = 0, stars_max = 5, price_min = 0, price_max = 10000, limit = 50, offset = 0, **data):
    if city:
        return {
            "stars_min": stars_min,
            "stars_max": stars_max,
            "price_min": price_min,
            "price_max": price_max,
            "city": city,
            "limit": limit,
            "offset": offset
        }
    return {
        "stars_min": stars_min,
        "stars_max": stars_max,
        "price_min": price_min,
        "price_max": price_max,
        "limit": limit,
        "offset": offset
    }

city_not_exists = """
    SELECT * FROM hoteis h
    WHERE (h.stars >= %s AND h.stars <= %s)
    AND (price >= %s AND price <= %s)
    LIMIT %s OFFSET %s
"""

city_exists = """
    SELECT * FROM hoteis h
    WHERE (h.stars >= %s AND h.stars <= %s)
    AND (price >= %s AND price <= %s)
    AND city = %s LIMIT %s OFFSET %s
"""