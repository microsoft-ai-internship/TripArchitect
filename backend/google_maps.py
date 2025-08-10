import os
import requests
from dotenv import load_dotenv
from typing import List, Tuple

load_dotenv()
GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_KEY")
if not GOOGLE_MAPS_KEY:
    raise RuntimeError("GOOGLE_MAPS_KEY environment variable is missing.")


def geocode_location(location_name: str) -> Tuple[float, float]:
    """Yer ismini enlem-boylam olarak döner."""
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": location_name,
        "key": GOOGLE_MAPS_KEY,
        "language": "tr"
    }
    res = requests.get(url, params=params)
    res.raise_for_status()
    data = res.json()

    if data["status"] != "OK" or not data["results"]:
        raise ValueError(f"'{location_name}' için koordinat bulunamadı.")

    loc = data["results"][0]["geometry"]["location"]
    return loc["lat"], loc["lng"]


def generate_route_url(locations: List[Tuple[float, float]]) -> str:
    """
    Koordinat listesinden Google Maps Directions embed URL'si üretir.
    locations: [(lat,lng), (lat,lng), ...] -- en az 2 nokta
    """
    if len(locations) < 2:
        raise ValueError("En az 2 koordinat olmalı.")

    origin = locations[0]
    destination = locations[-1]
    waypoints = locations[1:-1]

    waypoints_str = "|".join([f"{lat},{lng}" for lat, lng in waypoints]) if waypoints else ""

    url = (
        f"https://www.google.com/maps/embed/v1/directions"
        f"?key={GOOGLE_MAPS_KEY}"
        f"&origin={origin[0]},{origin[1]}"
        f"&destination={destination[0]},{destination[1]}"
    )
    if waypoints_str:
        url += f"&waypoints={waypoints_str}"
    url += "&language=tr"

    return url
