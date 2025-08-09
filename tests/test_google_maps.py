def test_route_api():
    api = GoogleMapsRouteAPI()
    result = api.get_optimized_route(["Ayasofya", "Topkapı Sarayı", "Sultanahmet"])
    assert result is not None
    assert len(result['waypoints']) >= 2

def test_link_generator():
    link = GoogleMapsLinkGenerator.generate_direct_link(["Ayasofya", "Topkapı"])
    assert link.startswith("https://www.google.com/maps/dir/")