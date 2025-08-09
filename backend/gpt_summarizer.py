import os
import openai
from dotenv import load_dotenv
from typing import List
from schemas import POI

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")


def generate_trip_description(pois: List[POI], budget: tuple, duration: int = 1) -> str:
    """GPT ile kişiselleştirilmiş gezi planı oluşturur"""
    try:
        prompt = f"""
        Kullanıcı için {duration} günlük bir gezi planı oluştur:
        - Bütçe: {budget[0]}-{budget[1]} TL
        - Mekanlar: {', '.join([poi.name for poi in pois])}
        - Türkçe ve maddeler halinde yaz
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "Sen bir profesyonel seyahat asistanısın."
            }, {
                "role": "user",
                "content": prompt
            }],
            temperature=0.7,
            max_tokens=500
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"GPT Hatası: {e}")
        return "\n".join([f"→ {poi.name}: {poi.types[0] if poi.types else 'Ziyaret noktası'}" for poi in pois[:3]])