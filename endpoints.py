import requests
from services import key_check, county_check, fetch_county_coordinates, fetch_data
from logging_config import setup_logging
from utils import coordinates_adjuster

# Set up logger
LOGGER = setup_logging()(__name__)

def search(key,county,country='USA'):
    try:
        if county:
            LOGGER.info(f"VERIFYING IF COUNTY : {county} IS PRESENT IN OUR DB")
            verified_county = county_check(county) # boolean parameter to ensure we have country present in DB
        else:
            LOGGER.info("COUNTY IS NOT FOUND IN DB")
            return []
        if key:
            LOGGER.info(f"VERIFYING IF KEY : {key} IS PRESENT IN OUR DB")
            verified_key = key_check(key) #boolean param to check if the key is a valid param

            if verified_key:
                LOGGER.info(f"County : {county} and Key : {key} are successfully found in DB")
                LOGGER.info(f"Searching coordinates for County : {county}")

                # fetch coordinates of the county from the DB in the form [success/failure, (coordinates)]
                coordinates_list = fetch_county_coordinates(county) 
                
                if coordinates_list: #TRUE
                    LOGGER.info(f"FOUND {coordinates_list} for COUNTY : {county}")
                    coordinates = coordinates_adjuster(coordinates_list) 
                    LOGGER.info(f"COORDINATES AFTER ADJUSTMENT : {coordinates}")
                    LOGGER.info(f"CALLING fetch_data service with \nKey: {key}\nCounty: {county} \nCoordinates:{coordinates}")
                    result = fetch_data(key=key,county=county,coordinates=coordinates) # [success/failure,[result]]
                    
                    if result[0]:
                        LOGGER.info("Result Fetched successfully for fetch_data in endpoints.py")
                        return result[1]
                    else:
                        return []
                else:
                    LOGGER.info(f"NO CORDINATES FOUND FOR COUNTY :{county}")
                    return []
            else:
                LOGGER.info("Key IS NOT FOUND IN DB")
                return []
            
    except Exception as e:
        LOGGER.info("THERE WAS SOME EXCEPTION",{e})
        return []        
    

