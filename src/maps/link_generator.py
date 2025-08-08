def generate_google_maps_link(origin, destination, waypoints=None):
    base_url = "https://www.google.com/maps/dir/?api=1"
    url = f"{base_url}&origin={origin}&destination={destination}"
    if waypoints:
        url += "&waypoints=" + "|".join(waypoints)
    return url

# Test örneği
if __name__ == "__main__":
    link = generate_google_maps_link("Istanbul", "Ankara", waypoints=["Bolu"])
    print(link)
