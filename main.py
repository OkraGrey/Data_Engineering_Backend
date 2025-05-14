from endpoints import search
from logging_config import setup_logging
from utils import records_cleaner
#Setting Up my LOGGER with Logging Level Info

LOGGER = setup_logging()(__name__)

if __name__ == "__main__":

    COUNTY = "Chilton"
    KEY    = "shop"
    LOGGER.info("Calling Search Endpoint")
    result = search(KEY,COUNTY) # Search takes Key and County where country = USA
    if len(result)>=1:

        LOGGER.info(f"SUCCESSFULLY FETCHED {len(result)} records for COUNTY : {COUNTY} and KEY : {KEY}")

        print(f"PRINTING RESULTS \n")
        
        # Data Quality
        # Given there are many fetched Records having no Name, Address and location, they are useless for any business case.
        # We are removing them.

        # Filtering only on Name Location (Lat, Lon) and Address
        # print(f"Length of fetched Records : {len(result)}")
        print(len(records_cleaner(result)))
    else:
        print("Search Operation returned Empty list")    



