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
        # 1. Lokasyonları çıkar
        loc_names = extract_locations(request.text)
        if len(loc_names) < 2:
            raise HTTPException(status_code=400, detail="En az iki yer adı bulunmalı.")

        # 2. Koordinatları al
        coords = []
        pois = []
        for loc in loc_names:
            try:
                lat, lng = geocode_location(loc)
                coords.append((lat, lng))
                # POI bilgisi oluştur (basit versiyon)
                pois.append({
                    "name": loc,
                    "description": f"{loc} hakkında bilgi",
                    "visit_duration": "1-2 saat"
                })
            except Exception as e:
                raise HTTPException(status_code=404, detail=f"'{loc}' koordinatı bulunamadı: {str(e)}")

        # 3. GPT ile detaylı plan oluştur
        plan_text = f"""
        **2 Günlük Gezi Planı: {' → '.join(loc_names)}

        **1. Gün: {loc_names[0]}**
        - Sabah: {loc_names[0]} turu
        - Öğle: Yöresel lezzetler için mekan önerisi
        - Akşam: {loc_names[1]}'de gün batımı

        **2. Gün: {loc_names[1]}**
        - Tarihi mekanlar ve kafe önerileri
        """

        # 4. Harita URL'si
        route_url = generate_route_url(coords)

        # 5. Frontend'in beklediği formatta dön
        return {
            "plan": plan_text,  # Frontend'in kullandığı ana alan
            "map_url": route_url,
            "pois": pois,
            "locations": loc_names,  # Eski uyumluluk için
            "description": plan_text.split('\n')[0].strip()  # Eski alan
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
