FETCH_CITIES = """SELECT * FROM CITIES c WHERE c.Id =?"""
VERIFY_AMENITY= "SELECT * FROM `amenities` a WHERE a.name = {amenity}"
COUNTY=  "SELECT * FROM `counties` c WHERE LOWER(c.COUNTY_NAME) = {county};"
VERIFY_KEY = "SELECT * FROM `osm_keys` k WHERE LOWER(k.key_name) = {key};"
GET_QUERY_ID = "SELECT query_id FROM queries WHERE county = %s AND `key` = %s"
GET_QUERY_ID_FOR_AMENITY= "SELECT query_id FROM amenity_queries WHERE county = %s AND `amenity` = %s"
FETCH_RECORDS_FROM_DB = """
SELECT name, brand, operator, phone, website, email, opening_hours, address, latitude, longitude FROM records WHERE query_id = %s;
"""
FETCH_AMENITY_RECORDS_FROM_DB = """
SELECT name, brand, operator, phone, website, email, opening_hours, address, latitude, longitude FROM amenity_records WHERE query_id = %s;
"""
INSERT_KEY_COUNTY = "INSERT INTO queries (county, `key`) VALUES (%s, %s)"
INSERT_AMENITY_COUNTY = "INSERT INTO amenity_queries (county, `amenity`) VALUES (%s, %s)"
INSERT_RECORDS_IN_DB = """
INSERT INTO records (
            query_id, name, brand, operator, phone, website, email, opening_hours,
            address, latitude, longitude
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
INSERT_AMENITY_RECORDS_IN_DB = """
INSERT INTO amenity_records (
            query_id, name, brand, operator, phone, website, email, opening_hours,
            address, latitude, longitude
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
MAIN_QUERY = """
[out:json][timeout:60];
(
  node[{key}]{coordinates};
  way[{key}]{coordinates};
  relation[{key}]{coordinates};
);
out center tags;
"""

MAIN_QUERY_AMENITIES = """
[out:json][timeout:60];
(
  node["amenity"={amenity}]{coordinates};
  way["amenity"={amenity}]{coordinates};
  relation["amenity"={amenity}]{coordinates};
);
out center tags;
"""