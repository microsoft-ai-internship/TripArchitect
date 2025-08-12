# backend/schemas.py
from pydantic import BaseModel
from typing import List, Optional

class Location(BaseModel):
    lat: float
    lng: float

class POI(BaseModel):
    name: str
    description: Optional[str] = None
    location: Optional[Location] = None
    visit_duration: Optional[str] = None