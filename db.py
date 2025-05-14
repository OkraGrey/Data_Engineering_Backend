from logging_config import setup_logging
import mysql.connector
import os
import dotenv 
from datetime import datetime
import requests
import json
import queries

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
    

# Data Checking 
def check_query_exists(county, key):
    LOGGER.info(f"check_query_exists called with county: {county}, key: {key}")
    LOGGER.info("INITIATING DATABASE CONNECTION")

    connection = mysql.connector.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DATABASE')
    )
    cursor = connection.cursor()
    
    LOGGER.info("EXECUTING QUERY TO CHECK EXISTENCE")
    query = 'SELECT query_id FROM queries WHERE county = %s AND `key` = %s'
    cursor.execute(queries.GET_QUERY_ID, (county, key))
    
    result = cursor.fetchone()
    
    LOGGER.info(f"Query result: {result}")

    LOGGER.info("Closing Connection")
    cursor.close()
    connection.close()

    return result[0] if result else None


def get_records(query_id):
    LOGGER.info(f"get_records called with query_id: {query_id}")
    LOGGER.info("INITIATING DATABASE CONNECTION")

    connection = mysql.connector.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DATABASE')
    )
    cursor = connection.cursor()
    
    LOGGER.info(f"EXECUTING QUERY TO FETCH RECORDS with QUERY_ID : {query_id}")
    cursor.execute(queries.FETCH_RECORDS_FROM_DB, (query_id,))

    rows = cursor.fetchall()
    
    LOGGER.info(f"Fetched {len(rows)} records")

    LOGGER.info("Closing Connection")
    cursor.close()
    connection.close()

    return [
        {
            'Name': row[0],
            'Brand': row[1],
            'Operator': row[2],
            'Phone': row[3],
            'Website': row[4],
            'Email': row[5],
            'Opening Hours': row[6],
            'Address': row[7],
            'Latitude': row[8],
            'Longitude': row[9]
        } for row in rows
    ]

def insert_query(county, key):
    LOGGER.info(f"insert_query called with county: {county}, key: {key}")
    LOGGER.info("INITIATING DATABASE CONNECTION")

    connection = mysql.connector.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DATABASE')
    )
    cursor = connection.cursor()

    LOGGER.info("EXECUTING INSERT QUERY")
    cursor.execute(queries.INSERT_KEY_COUNTY, (county, key))
    connection.commit()
    
    query_id = cursor.lastrowid
    LOGGER.info(f"Inserted query with ID: {query_id}")

    LOGGER.info("Closing Connection")
    cursor.close()
    connection.close()

    return query_id


def insert_records(query_id, records):
    LOGGER.info(f"insert_records called with query_id: {query_id} and {len(records)} records")
    LOGGER.info("INITIATING DATABASE CONNECTION")

    connection = mysql.connector.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DATABASE')
    )
    cursor = connection.cursor()

    LOGGER.info("EXECUTING INSERTS FOR RECORDS")

    for record in records:
        cursor.execute(queries.INSERT_RECORDS_IN_DB, (
            query_id,
            record['Name'],
            record['Brand'],
            record['Operator'],
            record['Phone'],
            record['Website'],
            record['Email'],
            record['Opening Hours'],
            record['Address'],
            record['Latitude'],
            record['Longitude']
        ))

    connection.commit()
    LOGGER.info("Records inserted successfully")

    LOGGER.info("Closing Connection")
    cursor.close()
    connection.close()

