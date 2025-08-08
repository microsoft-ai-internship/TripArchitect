import requests
from src.config import GOOGLE_MAPS_API_KEY

def get_route(origin, destination, waypoints=None, mode="driving"):
    """
    origin, destination: string adres veya "lat,lng" formatında
    waypoints: liste halinde yol üzerindeki duraklar (string listesi)
    mode: driving, walking, bicycling, transit
    """
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "key": GOOGLE_MAPS_API_KEY,
        "origin": origin,
        "destination": destination,
        "mode": mode
    }
    if waypoints:
        params["waypoints"] = "|".join(waypoints)

    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()

# Test örneği
if __name__ == "__main__":
    route = get_route("Istanbul", "Ankara", waypoints=["Bolu"])
    print(route)
