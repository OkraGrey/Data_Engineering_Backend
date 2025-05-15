from logging_config import setup_logging

# Set up logger
LOGGER = setup_logging()(__name__)

def build_query_with_amenities(query,amenity: str, coordinates: str) -> str:
    LOGGER.info(f"build_query is called with \nQuery: {query} \nAmenity: {amenity}\nCordinates:{coordinates}")
    return query.format(amenity=amenity, coordinates=coordinates)

def build_query_with_key(query,key: str, coordinates: str) -> str:
    LOGGER.info(f"build_query is called with \nQuery: {query} \nKey: {key}\nCordinates:{coordinates}")
    return query.format(key=key, coordinates=coordinates)

def build_amenity_query(query,amenity: str) -> str:
    LOGGER.info(f"build_amenity_query is called with \nQuery: {query} \nAmenity: {amenity}")
    return query.format(amenity=f"'{amenity}'")

def build_county_query(query,county: str) -> str:
    LOGGER.info(f"build_county_query is called with \nQuery: {query} \nCounty: {county}")
    return query.format(county=f"'{county}'")

def build_key_query(query,key: str) -> str:
    LOGGER.info(f"build_key_query is called with \nQuery: {query} \nKey: {key}")
    return query.format(key=f"'{key}'")

def coordinates_adjuster(coordinates: tuple) -> tuple:
    
    LOGGER.info(f"ORIGINAL COORDINATES: {coordinates}")
    original_min_lon, original_min_lat, original_max_lon, original_max_lat = coordinates

    # Clamp latitudes to [-90, 90]
    clamped_min_lat = max(-90.0, min(original_min_lat, 90.0))
    if clamped_min_lat != original_min_lat:
        LOGGER.info(f"min_lat clamped from {original_min_lat} to {clamped_min_lat}")
    else:
        LOGGER.info("NO CLAMPING FOR min_lat")
    clamped_max_lat = max(-90.0, min(original_max_lat, 90.0))

    if clamped_max_lat != original_max_lat:
        LOGGER.info(f"max_lat CLAMPED FROM {original_max_lat} TO {clamped_max_lat}")
    else:
        LOGGER.info("NO CLAMPING FOR max_lat")

    # Clamp longitudes to [-180, 180]/ Condition for Overpass Support
    clamped_min_lon = max(-180.0, min(original_min_lon, 180.0))
    if clamped_min_lon != original_min_lon:
        LOGGER.info(f"min_lon CLAMPED FROM {original_min_lon} TO {clamped_min_lon}")
    else:
        LOGGER.info("NO CLAMPING FOR min_lon")

    clamped_max_lon = max(-180.0, min(original_max_lon, 180.0))
    if clamped_max_lon != original_max_lon:
        LOGGER.info(f"max_lon CLAMPED FROM {original_max_lon} TO {clamped_max_lon}")
    else:
        LOGGER.info("NO CLAMPING FOR max_lon")

    south = min(clamped_min_lat, clamped_max_lat)
    north = max(clamped_min_lat, clamped_max_lat)

    west = clamped_min_lon
    east = clamped_max_lon

    adjusted_coordinates = (south, west, north, east)
    LOGGER.info(f"FINAL ADJUSTED COORDINATES: {adjusted_coordinates}")
    return adjusted_coordinates    
        

def records_cleaner(records:list):
    """
    Takes list of dictionaries as input and remove rows containing Unknown Name, Address. Location
    """
    return [element for element in records if element["Name"] !="Unknown" and element["Address"] !="Unknown" and element["Latitude"] !="Unknown" and element["Longitude"] !="Unknown"]