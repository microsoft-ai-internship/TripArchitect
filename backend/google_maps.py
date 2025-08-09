import os
import requests
from dotenv import load_dotenv
from schemas import POI, Location
from typing import List

load_dotenv()


def search_places(location: str, radius: int, types: str, maxprice: int = None) -> List[POI]:
    """Google Places API'den genel arama fonksiyonu"""
    params = {
        "location": location,
        "radius": radius,
        "type": types,
        "key": os.getenv("GOOGLE_MAPS_KEY"),
        "language": "tr"
    }
    if maxprice:
        params["maxprice"] = maxprice

    response = requests.get("https://maps.googleapis.com/maps/api/place/nearbysearch/json", params=params)
    results = response.json().get("results", [])

    return [
        POI(
            name=place["name"],
            location=Location(**place["geometry"]["location"]),
            rating=place.get("rating"),
            types=place.get("types", [])
        )
        for place in results
    ]


def get_place_photo(photo_reference: str, max_width=400) -> str:
    """Place fotoğraf URL'si oluşturur"""
    return f"https://maps.googleapis.com/maps/api/place/photo?maxwidth={max_width}&photo_reference={photo_reference}&key={os.getenv('GOOGLE_MAPS_KEY')}"


def generate_route_url(origin: Location, destination: Location, waypoints: List[Location]) -> str:
    """Google Maps Directions embed URL oluşturur"""
    waypoints_str = "|".join([f"{wp.lat},{wp.lng}" for wp in waypoints])
    return f"https://www.google.com/maps/embed/v1/directions?key={os.getenv('GOOGLE_MAPS_KEY')}&origin={origin.lat},{origin.lng}&destination={destination.lat},{destination.lng}&waypoints={waypoints_str}&language=tr"