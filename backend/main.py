from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from nlp_handler import extract_intent
from google_maps import search_places, generate_route_url
from gpt_summarizer import generate_trip_description
from schemas import POI, TripPlanResponse
import os

app = FastAPI(title="TripArchitect API")

# CORS Ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TripRequest(BaseModel):
    text: str


@app.post("/plan_trip", response_model=TripPlanResponse)
async def plan_trip(request: TripRequest):
    try:
        # NLP ile intent çıkarımı
        intent = extract_intent(request.text)

        # Google Maps'ten veri çekme
        location = "41.025,28.974"  # Beşiktaş koordinatları
        hotels = search_places(location, 2000, "lodging", intent["budget"][1])
        pois = search_places(location, 5000, "|".join(intent["categories"]))

        # Rota URL'si oluşturma
        route_url = generate_route_url(
            origin=pois[0].location,
            destination=pois[-1].location,
            waypoints=[poi.location for poi in pois[1:-1]]
        )

        # GPT ile açıklama oluşturma
        description = generate_trip_description(pois, intent["budget"], intent["duration"])

        return TripPlanResponse(
            hotels=hotels[:3],
            pois=pois[:5],
            description=description,
            map_url=route_url
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)