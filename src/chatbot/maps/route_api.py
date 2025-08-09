import googlemaps
from src.chatbot.config import GOOGLE_MAPS_API_KEY


class GoogleMapsRouteAPI:
    def __init__(self):
        self.client = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

    def get_optimized_route(self, locations: list[str], mode="walking"):
        """Lokasyonları coğrafi olarak optimize eder"""
        if len(locations) < 2:
            return None

        try:
            result = self.client.directions(
                origin=locations[0],
                destination=locations[-1],
                waypoints=locations[1:-1],
                mode=mode,
                optimize_waypoints=True,
                language="tr"
            )
            return {
                'waypoints': [step['start_address'] for step in result[0]['legs']] + [
                    result[0]['legs'][-1]['end_address']],
                'duration': sum(leg['duration']['value'] for leg in result[0]['legs']),
                'distance': sum(leg['distance']['value'] for leg in result[0]['legs'])
            }
        except Exception as e:
            print(f"Rota API hatası: {e}")
            return None