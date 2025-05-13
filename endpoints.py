import requests
import logging as LOGGER

def search(amenity,county,country='USA'):
    try:
        if county:
            LOGGER.info(f"VERIFYING IF COUNTY : {county} IS PRESENT IN OUR DB")
            verified_county = county_check(county) # boolean parameter to ensure we have country present in DB
        else:
            LOGGER.info("COUNTY IS NOT FOUND IN DB")
            return []
        if amenity:
            LOGGER.info(f"VERIFYING IF AMENITY : {amenity} IS PRESENT IN OUR DB")
            verified_amenity = amenity_check(amenity) #boolean param to check if the amenity is a valid param

            if verified_county and verified_amenity:
                LOGGER.info(f"County : {county} and Amenity : {amenity} are successfully found in DB")
                
                LOGGER.info(f"Searching coordinates for County : {county}")

                # fetch coordinates of the county from the DB in the form [success/failure, (coordinates)]
                coordinates_list = fetch_county_coordinates(county) 
                
                if coordinates_list[0]: #TRUE
                    LOGGER.info(f"FOUND {coordinates} for COUNTY : {county}")
                    coordinates = coordinates_list[1] # Extract coordinates in a tuple format
                    LOGGER.info(f"CALLING fetch_amenities service with \nAmenity: {amenity}\nCounty: {county} \nCoordinates:{coordinates}")
                    result = fetch_amentities(amenity=amenity,county=county,coordinates=coordinates) # [success/failure,[result]]
                    
                    if result[0]:
                        LOGGER.info("Result Fetched successfully for fetch_amentities in endpoints.py")
                        return result[1]
                    else:
                        return []
                else:
                    LOGGER.info(f"NO CORDINATES FOUND FOR AMENITY :{amenity}")
                    return []
            else:
                LOGGER.info("AMENITY IS NOT FOUND IN DB")
                return []
            
    except Exception as e:
        LOGGER.info("THERE WAS SOME EXCEPTION",{e})
        return []        