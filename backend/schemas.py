from pydantic import BaseModel
from typing import List, Optional

class Location(BaseModel):
    lat: float
    lng: float

class POI(BaseModel):
    name: str
    location: Location
    rating: Optional[float]
    types: List[str]

class TripPlanResponse(BaseModel):
    hotels: List[POI]
    pois: List[POI]
    description: str
    map_url: str