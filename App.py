from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
from mysql.connector import pooling
from endpoints import search, search_amenity
from logging_config import setup_logging
from utils import records_cleaner
from db import check_query_exists, get_records, insert_query,insert_amenity_records, insert_amenity_query, insert_records, get_amenity_records, create_connection, get_connection_pool,check_query_with_amenity_exists
from dotenv import load_dotenv
import os
#Setting Up my LOGGER with Logging Level Info

LOGGER = setup_logging()(__name__)
load_dotenv()
# Thread-local storage for database connections

CONNECTION_POOL = get_connection_pool()

def wrapper(county, key):
    """Process a single county-key combination and return fetch/save counts."""
    LOGGER.info(f"Starting {county}:{key}")
    connection = create_connection(CONNECTION_POOL)
    query_id = check_query_exists(county, key, connection)
    records = None
    fetched_count = 0
    saved_count = 0
    records = []
    if query_id:
        LOGGER.info(f"{county}:{key} - Records already exist in DB")
        records = get_records(query_id, connection)
        fetched_count = len(records) if records else 0
        saved_count = fetched_count  # No new saves since it’s from DB
        print(f"EXECUTION COMPLETE WITH FETCHING {fetched_count} records from DB")
        return records
    else:
        LOGGER.info(f"{county}:{key} - Fetching from API")
        records = search(key, county)
        fetched_count = len(records) if records else 0
        if records:
            query_id = insert_query(county, key, connection)
            cleaned_records = records_cleaner(records)
            saved_count = len(cleaned_records)
            insert_records(query_id, cleaned_records, connection)
            LOGGER.info(f"{county}:{key} - Saved successfully ({saved_count} records)")
            print(f"EXECUTION COMPLETE WITH FETCHING {len(cleaned_records)} Cleaned Records from OVERPASS API")
            return cleaned_records
        else:
            LOGGER.info(f"{county}:{key} - No records to save from API")
    
    return records

def amenity_wrapper(county,amenity):

    LOGGER.info(f"Starting AMENITY WRAPPER with params County :{county} and AMENITY :{amenity}")
    connection = create_connection(CONNECTION_POOL)
    query_id = check_query_with_amenity_exists(county, amenity, connection)
    records = None
    fetched_count = 0
    saved_count = 0
    records = []
    if query_id:
        LOGGER.info(f"FOR county: {county} and Amenity :{amenity} - Records already exist in DB")
        records = get_amenity_records(query_id, connection)
        fetched_count = len(records) if records else 0
        saved_count = fetched_count  # No new saves since it’s from DB
        print(f"EXECUTION COMPLETE WITH FETCHING {fetched_count} records from DB")
        return records
    else:
        LOGGER.info(f"{county}:{amenity} - Fetching from API")
        records = search_amenity(amenity, county)
        fetched_count = len(records) if records else 0
        if records:
            query_id = insert_amenity_query(county=county, amenity=amenity, connection=connection)
            cleaned_records = records_cleaner(records)
            saved_count = len(cleaned_records)
            insert_amenity_records(query_id, cleaned_records, connection)
            LOGGER.info(f"{county}:{amenity} - Saved successfully ({saved_count} records)")
            print(f"EXECUTION COMPLETE WITH FETCHING {len(cleaned_records)} Cleaned Records from OVERPASS API")
            return cleaned_records
        else:
            LOGGER.info(f"{county}:{amenity} - No records to save from API")
    
    return records

def long_search(counties: list, keys: list, max_workers: int = 5):

    if not counties or not keys:
        raise ValueError("Counties or keys list cannot be empty")

    start_time = time.time()
    total_fetched = 0
    total_saved = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_combination = {
            executor.submit(wrapper, county, key): (county, key)
            for county in counties
            for key in keys
        }
        
        for future in as_completed(future_to_combination):
            try:
                result = future.result()
                # print(f'RESULT OF THREAD :\n County: {result["county"]}, Key: {result["key"]} , Fetched: {result["fetched"]}, Saved: {result["saved"]}')
                total_fetched += len(result)
                # total_saved += result["saved"]
            except Exception as e:
                county, key = future_to_combination[future]
                LOGGER.error(f"Error processing {county}:{key} - {e}")

    total_time = time.time() - start_time
    LOGGER.info(f"Completed: Fetched {total_fetched}, Saved {total_saved}, Time: {total_time:.2f}s")

    return {
        "total_fetched": total_fetched,
        # "total_saved": total_saved,
        "total_time": total_time
    }
             





