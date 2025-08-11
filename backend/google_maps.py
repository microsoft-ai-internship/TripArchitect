import os
import requests
from dotenv import load_dotenv
from typing import List, Tuple
from urllib.parse import quote  # Yeni eklenen satır

load_dotenv()

GOOGLE_MAPS_KEY = os.getenv("GOOGLE_MAPS_KEY")
if not GOOGLE_MAPS_KEY:
    raise RuntimeError("GOOGLE_MAPS_KEY environment variable is missing.")


def geocode_location(location_name: str) -> Tuple[float, float]:
    """Geliştirilmiş lokasyon arama"""
    # Önce doğrudan arama yap
    try:
        return _geocode(location_name)
    except ValueError:
        # Fallback: İstanbul ekleyerek tekrar dene
        if "İstanbul" not in location_name:
            try:
                return _geocode(f"{location_name}, İstanbul")
            except ValueError:
                raise ValueError(f"'{location_name}' için koordinat bulunamadı (İstanbul eklenerek de denendi)")


def _geocode(location_name: str) -> Tuple[float, float]:
    """Gerçek API çağrısı"""
    encoded_name = quote(location_name)
    params = {
        "address": encoded_name,
        "key": GOOGLE_MAPS_KEY,
        "language": "tr",
        "region": "tr"
    }
    res = requests.get("https://maps.googleapis.com/maps/api/geocode/json", params=params)
    data = res.json()

    if data["status"] != "OK":
        raise ValueError(data.get("error_message", "Bilinmeyen hata"))

    loc = data["results"][0]["geometry"]["location"]
    return (loc["lat"], loc["lng"])


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
