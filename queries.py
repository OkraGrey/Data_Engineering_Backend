FETCH_CITIES = """SELECT * FROM CITIES c WHERE c.Id =?"""
VERIFY_AMENITY= "SELECT * FROM `amenities` a WHERE a.name = {amenity}"
COUNTY=  "SELECT * FROM `counties` c WHERE c.COUNTY_NAME = {county};"
VERIFY_KEY = "SELECT * FROM `osm_keys` k WHERE LOWER(k.key_name) = {key};"
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