from logging_config import setup_logging
import mysql.connector
import os
import dotenv 
from datetime import datetime
import requests
import json

# Set up logger
LOGGER = setup_logging()(__name__)

#Loading .env
dotenv.load_dotenv()

def query_executor(query):
    
    LOGGER.info(f"query_executor is called with Query : {query}")
    # Connect to the MySQL database
    LOGGER.info("INITIATING DATABASE CONNECTION")    
    
    connection = mysql.connector.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DATABASE')
    )
    cursor = connection.cursor()
    LOGGER.info("EXECUTING QUERY")
    cursor.execute(query)
    results = cursor.fetchall()
    LOGGER.info(f"FETCHED RESULTS : {results}")

    LOGGER.info("Closing Connection")
    cursor.close()
    connection.close()

    return results
    # Clean up


# Overpass API endpoint
url = "http://overpass-api.de/api/interpreter"

# Query to get all fuel stations in the specified bounding box
query = """
[out:json][timeout:3600];
(
  node["amenity"="taxi"]((32.5121, -124.6509, 42.0126, -114.1312));
  way["amenity"="taxi"](32.5121, -124.6509, 42.0126, -114.1312));
  relation["amenity"="taxi"]((32.5121, -124.6509, 42.0126, -114.1312));
);
out center tags;
"""
def fetch_from_overpass(query):

    # Send POST request to Overpass API
    response = requests.post(url, data={'data': query})
    results = []
    # Check response
    if response.status_code == 200:
        data = response.json()
        LOGGER.info(f"RECEIVED RESPONSE FROM OVERPASS : \n {data}")
        # with open('business_profiles.txt', 'w', encoding='utf-8') as file:
        for el in data['elements']:
            tags = el.get('tags', {})

            name = tags.get('name', 'Unknown')
            brand = tags.get('brand', 'Unknown')
            operator = tags.get('operator', 'Unknown')
            phone = tags.get('phone', tags.get('contact:phone', 'Unknown'))
            website = tags.get('website', tags.get('contact:website', 'Unknown'))
            email = tags.get('email', tags.get('contact:email', 'Unknown'))
            opening_hours = tags.get('opening_hours', 'Unknown')
            addr_street = tags.get('addr:street', '')
            addr_housenumber = tags.get('addr:housenumber', '')
            addr_city = tags.get('addr:city', '')
            addr_postcode = tags.get('addr:postcode', '')

            address = ', '.join(filter(None, [addr_housenumber, addr_street, addr_city, addr_postcode])) or "Unknown"

            # Get location for nodes or center for ways/relations
            lat = el.get('lat') or el.get('center', {}).get('lat', 'Unknown')
            lon = el.get('lon') or el.get('center', {}).get('lon', 'Unknown')

            profile = {
                "Name": name,
                "Brand": brand,
                "Operator": operator,
                "Phone": phone,
                "Website": website,
                "Email": email,
                "Opening Hours": opening_hours,
                "Address": address,
                "Latitude": lat,
                "Longitude": lon
                }
            results.append(profile)
                # print(profile)
                # file.write(profile + '\n')
        return results
    else:
        LOGGER.info(f"THERE WAS SOME ERROR IN OVERPASS RESPONSE: \n {response.content}")
    
