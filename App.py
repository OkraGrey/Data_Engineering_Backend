from endpoints import search
from logging_config import setup_logging
from utils import records_cleaner
from db import check_query_exists, get_records, insert_query, insert_records
#Setting Up my LOGGER with Logging Level Info

LOGGER = setup_logging()(__name__)

def wrapper(county, key):
    # COUNTY = "Chilton"
    # KEY    = "shop"
    LOGGER.info("Calling Search Endpoint")

    query_id = check_query_exists(county, key)
    records = None

    if query_id:
        LOGGER.info(f"Query for {county} and {key} found in database")
        # Incase we do have data in DB, we will fetch it from DB
        records = get_records(query_id)
        LOGGER.info(f"Retrieved {len(records)} records from database")
    else:# In case ww don't find one, we will fetch from tradional way
        LOGGER.info(f"No query found for {county} and {key}, performing search")
        records = search(key, county)
        query_id = insert_query(county, key)
        if records:
            cleaned_records = records_cleaner(records)
            LOGGER.info(f"After cleaning, {len(cleaned_records)} records remain")
            insert_records(query_id, cleaned_records)
            LOGGER.info(f"Inserted {len(cleaned_records)} records into database")
        else:
            LOGGER.info("Search returned no records, but query is recorded")
    return records



