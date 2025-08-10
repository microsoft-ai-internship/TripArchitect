import os
import openai
from dotenv import load_dotenv
from typing import List
from schemas import POI

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")
if not OPENAI_KEY:
    raise RuntimeError("OPENAI_KEY environment variable is missing.")

openai.api_key = OPENAI_KEY

def generate_trip_description(pois: List[POI], budget: tuple, duration: int = 1) -> str:
    """GPT ile kişiselleştirilmiş gezi planı oluşturur."""
    try:
        prompt = f"""
        Kullanıcı için {duration} günlük bir gezi planı oluştur:
        - Bütçe: {budget[0]}-{budget[1]} TL
        - Mekanlar: {', '.join([poi.name for poi in pois])}
        - Türkçe ve maddeler halinde yaz.
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen bir profesyonel seyahat asistanısın."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"GPT Hatası: {e}")
        return "\n".join([
            f"→ {poi.name}: {poi.types[0] if poi.types else 'Ziyaret noktası'}"
            for poi in pois[:3]
        ])

if __name__ == "__main__":
    from schemas import POI, Location
    sample_pois = [
        POI(name="Topkapı Sarayı", location=Location(lat=41.012, lng=28.983), rating=4.6, types=["museum"]),
        POI(name="Ayasofya", location=Location(lat=41.008, lng=28.980), rating=4.7, types=["museum"]),
    ]
    print(generate_trip_description(sample_pois, (3000, 5000), 2))
