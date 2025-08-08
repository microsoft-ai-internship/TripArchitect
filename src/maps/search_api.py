import requests
from src.config import GOOGLE_MAPS_API_KEY

def search_places(query, location, radius=5000):

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "key": GOOGLE_MAPS_API_KEY,
        "location": f"{location[0]},{location[1]}",
        "radius": radius,
        "keyword": query
    }
    response = requests.get(url, params=params)
    return response.json()
