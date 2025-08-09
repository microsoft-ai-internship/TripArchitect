from urllib.parse import quote
from src.chatbot.config import GOOGLE_MAPS_API_KEY

class GoogleMapsLinkGenerator:
    @staticmethod
    def generate_direct_link(locations: list[str]) -> str:
        """Tıklanabilir direkt link oluşturur"""
        base = "https://www.google.com/maps/dir/"
        encoded = [quote(loc) for loc in locations]
        return f"{base}{'/'.join(encoded)}"

    @staticmethod
    def generate_embed_link(locations: list[str]) -> str:
        """Embed harita linki oluşturur"""
        base = "https://www.google.com/maps/embed/v1/directions"
        params = {
            'key': GOOGLE_MAPS_API_KEY,
            'origin': locations[0],
            'destination': locations[-1],
            'waypoints': '|'.join(locations[1:-1]) if len(locations) > 2 else '',
            'mode': 'walking'
        }
        return f"{base}?{'&'.join(f'{k}={v}' for k,v in params.items() if v)}"