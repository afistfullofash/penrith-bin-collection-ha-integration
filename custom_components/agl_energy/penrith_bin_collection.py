import httpx
import functools
import json

def get_endpoint(website, endpoint):
    r = httpx.get(f"{website}{endpoint}")
    return(r.text)

get_url = functools.partial(get_endpoint, WEBSITE_URL)

def get_localities():
    return json.loads(get_url("localities.json"))["localities"]

def find_locality(localities, locality_name):
    return [locality for locality in localities if locality["name"] == locality_name][0]

def get_street(locality_id):
    return json.loads(get_url(f"streets.json?locality={locality_id}"))["streets"]

def find_street(streets, street_name):
    return [street for street in streets if street["name"] == street_name][0]

def get_properties(street_id):
    return json.loads(get_url(f"properties.json?street={street_id}"))["properties"]

def find_property(properties, property_name):
    return [property for property in properties if property["name"] == property_name][0]

def get_calendar(property_id, start="2024-12-31T13:00:00.000Z", end="2025-12-30T13:00:00.000Z"):
    dates = json.loads(get_url(f"properties/{property_id}.json?start={start}&end={end}"))
    grouped_by_event = defaultdict(list)
    for event in dates:
        key = event["event_type"]
        grouped_by_event[key].append(event)
    return grouped_by_event


