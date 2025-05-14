from logging_config import setup_logging

# Set up logger
LOGGER = setup_logging()(__name__)

def build_query(query,amenity: str, coordinates: str) -> str:
    LOGGER.info(f"build_query is called with \nQuery: {query} \nAmenity: {amenity}\nCordinates:{coordinates}")
    return query.format(amenity=amenity, coordinates=coordinates)

def build_amenity_query(query,amenity: str) -> str:
    LOGGER.info(f"build_amenity_query is called with \nQuery: {query} \nAmenity: {amenity}")
    return query.format(amenity=f"'{amenity}'")

def build_county_query(query,county: str) -> str:
    LOGGER.info(f"build_county_query is called with \nQuery: {query} \nAmenity: {county}")
    return query.format(county=f"'{county}'")