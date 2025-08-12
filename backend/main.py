# backend/main.py
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

from gpt_summarizer import parse_user_text_to_structure, generate_place_descriptions
from google_maps import geocode_location, generate_route_url
from schemas import POI, Location

app = FastAPI(title="TripArchitect API")

# CORS - geliştirme sırasında * kullanımı kolay; prod'da frontend origin'ini belirt.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

class TripRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "TripArchitect API çalışıyor 🚀"}

@app.post("/plan_trip")
async def plan_trip(request: TripRequest):
    """
    Workflow:
    1) Kullanıcının serbest metnini GPT'ye ver -> yapılandırılmış JSON (days, start,end,stops, budget)
    2) stops listesindeki mekanları geocode et (koordinatlar)
    3) Her mekan için kısa açıklama üret (2-4 cümle) — GPT
    4) route_url oluştur ve JSON döndür
    """
    try:
        user_text = request.text.strip()
        if not user_text:
            raise HTTPException(status_code=400, detail="Metin boş olamaz.")

        # 1) Parse user text -> struct
        struct = parse_user_text_to_structure(user_text)

        days = struct.get("days")
        start = struct.get("start_location")
        end = struct.get("end_location")
        budget = struct.get("budget")
        stops_by_day = struct.get("stops", [])  # örn: [ ["A","B"], ["C","D"] ]

        # Eğer stops_by_day boşsa, hata ver veya fallback mekan üret (model sorunsuz yapmalı)
        if not stops_by_day:
            raise HTTPException(status_code=400, detail="Rota için yeterli durak çıkartılamadı. Lütfen isteği biraz daha ayrıntılı verin.")

        # 2) Düz bir mekan listesi (sıralı) ve unique list
        flat_stops = []
        for day in stops_by_day:
            for s in day:
                if s not in flat_stops:
                    flat_stops.append(s)

        # 3) Koordinatları al (başarısızsa hata tut)
        coords = []
        pois: List[POI] = []
        failed = []
        for name in flat_stops:
            try:
                lat, lng = geocode_location(name)
                coords.append((lat, lng))
                pois.append(POI(
                    name=name,
                    location=Location(lat=lat, lng=lng),
                    visit_duration=None
                ))
            except Exception as e:
                failed.append({"name": name, "error": str(e)})

        if not coords:
            raise HTTPException(status_code=404, detail=f"Hicbir mekan için koordinat bulunamadı. Hata örnekleri: {failed[:3]}")

        # 4) Her POI için kısa açıklamalar (2-4 cümle)
        place_names = [p.name for p in pois]
        descriptions_map = generate_place_descriptions(place_names)

        # Update POIs with descriptions
        for p in pois:
            if p.name in descriptions_map:
                p.description = descriptions_map[p.name]
            else:
                p.description = f"{p.name} hakkında bilgi bulunamadı."

        # 5) Harita URL (Google Embed)
        route_url = generate_route_url(coords)

        # 6) Çıktı düzeni
        out = {
            "plan": struct.get("notes") or "",   # modelin 'plan' ya da 'notes' alanı varsa oradan al
            "days": days,
            "start_location": start,
            "end_location": end,
            "budget": budget,
            "stops_by_day": stops_by_day,
            "pois": [p.dict() for p in pois],
            "map_url": route_url
        }

        return out

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sunucu hatası: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)