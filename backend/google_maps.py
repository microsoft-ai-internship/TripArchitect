# backend/google_maps.py
import os
import requests
from dotenv import load_dotenv
from typing import List, Tuple
from urllib.parse import quote_plus

load_dotenv()

GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_KEY")
if not GOOGLE_MAPS_KEY:
    raise RuntimeError("GOOGLE_MAPS_KEY environment variable is missing.")

def geocode_location(location_name: str) -> Tuple[float, float]:
    """
    Verilen yer adını Google Geocoding API ile enlem-boylam döner.
    Eğer doğrudan bulunamazsa, lokasyona şehir/ülke ekleyerek tekrar dener.
    """
    location_name = location_name.strip()
    try:
        return _geocode(location_name)
    except ValueError:
        # Deneme: lokasyona Türkiye ekle (ör: "Nilüfer" -> "Nilüfer, Bursa, Türkiye")
        try:
            return _geocode(f"{location_name}, Türkiye")
        except ValueError:
            raise ValueError(f"'{location_name}' için koordinat bulunamadı.")

def _geocode(location_name: str) -> Tuple[float, float]:
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": location_name,
        "key": GOOGLE_MAPS_KEY,
        "language": "tr",
        "region": "tr"
    }
    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    data = res.json()

    if data.get("status") != "OK" or not data.get("results"):
        raise ValueError(data.get("error_message") or data.get("status") or "Koordinat bulunamadı")

    loc = data["results"][0]["geometry"]["location"]
    return (loc["lat"], loc["lng"])

def generate_route_url(locations: List[Tuple[float, float]]) -> str:
    """
    Google Maps Embed Directions URL üretir.
    locations: [(lat,lng), (lat,lng), ...]  (en az 2 adet)
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
        url += f"&waypoints={quote_plus(waypoints_str)}"
    url += "&language=tr"

    return url