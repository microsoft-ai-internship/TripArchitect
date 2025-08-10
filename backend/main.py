from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from nlp_handler import extract_locations
from google_maps import geocode_location, generate_route_url

app = FastAPI(title="TripArchitect API")

# --- CORS ayarları ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Gerekirse buraya sadece frontend URL'ini yaz
    allow_methods=["*"],
    allow_headers=["*"],
)

class TripRequest(BaseModel):
    text: str

@app.post("/plan_trip")
async def plan_trip(request: TripRequest):
    try:
        # 1. Metinden yer adlarını çıkar
        loc_names = extract_locations(request.text)
        if len(loc_names) < 2:
            raise HTTPException(status_code=400, detail="En az iki yer adı bulunmalı.")

        # 2. Yerleri koordinatlara çevir
        coords = []
        for loc in loc_names:
            try:
                latlng = geocode_location(loc)
                coords.append(latlng)
            except Exception as e:
                raise HTTPException(status_code=404, detail=f"'{loc}' koordinatı bulunamadı: {str(e)}")

        # 3. Google Maps URL'si oluştur
        route_url = generate_route_url(coords)

        # 4. Basit açıklama
        description = f"Gezi rotası: {' -> '.join(loc_names)}"

        # 5. JSON formatında dön (frontend uyumlu)
        return {
            "locations": loc_names,
            "map_url": route_url,
            "description": description,
            "hotels": [],
            "pois": []
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
