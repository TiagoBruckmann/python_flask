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
    WHERE (h.stars >= ? AND h.stars <= ?)
    AND (price >= ? AND price <= ?)
    LIMIT ? OFFSET ?
"""

city_exists = """
    SELECT * FROM hoteis h
    WHERE (h.stars >= ? AND h.stars <= ?)
    AND (price >= ? AND price <= ?)
    AND city = ? LIMIT ? OFFSET ?
"""