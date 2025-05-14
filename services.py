import queries
from utils import build_amenity_query, build_county_query,build_query_with_key, build_key_query
from db import query_executor, fetch_from_overpass
from logging_config import setup_logging
# Set up logger

LOGGER = setup_logging()(__name__)

def county_check(county):
    LOGGER.info(f"county_check Service is called with param :{county}")
    Query = build_county_query(queries.COUNTY,county=county)
    LOGGER.info(f"query_executor to be called with \nQUERY : {Query}")
    result = query_executor(Query)
    if len(result)>=1:
        return True
    else:
        return False


def key_check(key):
    LOGGER.info(f"key_check service is called with {key} param")
    Query = build_key_query(query=queries.VERIFY_KEY,key=key)
    LOGGER.info(f"query_executor to be called with \nQUERY : {Query}")
    result = query_executor(Query)
    if len(result) == 1:
        return True
    else:
        return False

    # return True

def fetch_county_coordinates(county):
    LOGGER.info(f"fetch_county_coordinates Service is called with param :{county}")
    Query = build_county_query(queries.COUNTY,county=county)
    LOGGER.info(f"query_executor to be called with \nQUERY : {Query}")
    result = query_executor(Query)
    if len(result)>=1:
        return (result[0][4],result[0][5],result[0][6],result[0][7])
    # No need for else case.

def fetch_data(key,county,coordinates):
    LOGGER.info(f"fetch_amenities Service is called with \nparamas : Key :{key}, County: {county}, Coordinates : {coordinates}")
    Query = build_query_with_key(query=queries.MAIN_QUERY, key=key,coordinates=coordinates)
    LOGGER.info(f"QUERY GENERATED : {Query}")
    result = fetch_from_overpass(Query) 
    if len(result) >=1:
        return [True,result]
    else:
        return [False,result]
    # print(result)