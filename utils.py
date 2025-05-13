import logging as LOGGER

def build_query(query,amenity: str, coordinates: str) -> str:
    LOGGER.info(f"build_query is called with \nQuery: {query} \nAmenity: {amenity}\nCordinates:{coordinates}")
    return query.format(amenity=amenity, coordinates=coordinates)