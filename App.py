from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
from mysql.connector import pooling
from endpoints import search
from logging_config import setup_logging
from utils import records_cleaner
from db import check_query_exists, get_records, insert_query, insert_records
from dotenv import load_dotenv
import os
#Setting Up my LOGGER with Logging Level Info

LOGGER = setup_logging()(__name__)
load_dotenv()
# Thread-local storage for database connections
thread_local = threading.local()

# MySQL connection pool configuration
DB_CONFIG = {
    "host": os.getenv("HOST"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "database": os.getenv("DATABASE"),
    "pool_name": "mypool",
    "pool_size": 10 
}

# Create a connection pool
connection_pool = pooling.MySQLConnectionPool(**DB_CONFIG)

def create_connection():
    """
    Get or create a database connection from the pool for the current thread.
    
    Returns:
        MySQLConnection: A thread-local database connection
    """
    if not hasattr(thread_local, "connection"):
        thread_local.connection = connection_pool.get_connection()
    return thread_local.connection

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

        if records:
            query_id = insert_query(county, key)
            cleaned_records = records_cleaner(records)
            LOGGER.info(f"After cleaning, {len(cleaned_records)} records remain")
            insert_records(query_id, cleaned_records)
            LOGGER.info(f"Inserted {len(cleaned_records)} records into database")
        else:
            LOGGER.info("Search returned no records, but query is recorded")
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
                print(f'RESULT OF THREAD : {result}')
                total_fetched += result["fetched"]
                total_saved += result["saved"]
            except Exception as e:
                county, key = future_to_combination[future]
                LOGGER.error(f"Error processing {county}:{key} - {e}")

    total_time = time.time() - start_time
    LOGGER.info(f"Completed: Fetched {total_fetched}, Saved {total_saved}, Time: {total_time:.2f}s")

    return {
        "total_fetched": total_fetched,
        "total_saved": total_saved,
        "total_time": total_time
    }
             



