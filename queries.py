FETCH_CITIES = """SELECT * FROM CITIES c WHERE c.Id =?"""

MAIN_QUERY = """
[out:json][timeout:3600];
(
  node["amenity"={amenity}]({coordinates});
  way["amenity"={amenity}]({coordinates});
  relation["amenity"={amenity}]({coordinates});
);
out center tags;
"""