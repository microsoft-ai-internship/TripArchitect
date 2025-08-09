from typing import List
from src.chatbot.maps import GoogleMapsAPI


def optimize_route(locations: List[str]) -> List[str]:
    if not locations:
        raise ValueError("Lokasyon listesi boş olamaz")
    if len(locations) < 2:
        return locations

    try:
        gmaps = GoogleMapsAPI()
        return gmaps.get_optimized_route(locations)
    except Exception as e:
        print(f"Optimizasyon hatası: {str(e)}")
        return locations