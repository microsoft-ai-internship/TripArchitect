import openai
from typing import List
import re
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_KEY")
if not OPENAI_KEY:
    raise RuntimeError("OPENAI_KEY environment variable is missing.")

import openai
openai.api_key = OPENAI_KEY

def extract_locations(text: str) -> List[str]:
    """
    Metinden lokasyonları çıkarır (GPT-3.5 ile geliştirilmiş versiyon).
    Örnek: "Beşiktaş'tan başlayarak 2 günlük İstanbul gezisi" → ["Beşiktaş", "İstanbul"]
    """
    try:
        prompt = f"""
        Aşağıdaki metinde geçen tüm şehir, ilçe, semt veya turistik yer adlarını Türkçe olarak listele.
        Çıktı sadece virgülle ayrılmış isimler olsun. Örnek: 'İstanbul,Beşiktaş,Sultanahmet'

        METİN: {text}
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen bir coğrafi lokasyon çıkarıcısısın. Sadece yer isimlerini listele."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=100
        )

        text_response = response.choices[0].message.content.strip()
        locations = [
            loc.strip()
            for loc in re.split(r",|\n", text_response)
            if loc.strip() and len(loc.strip()) > 2
        ]

        return locations[:6]

    except Exception as e:
        print(f"NLP Hatası: {e}")
        return []

def get_tourist_spots(start: str, end: str, count: int = 5) -> List[str]:
    """
    Başlangıç ve bitiş lokasyonları arasında, count kadar
    gezilecek yer önerisi alır.
    """
    try:
        prompt = f"""
        İstanbul'da '{start}' ve '{end}' arasında gezilebilecek
        tarihi ve turistik {count} yer adı listele.
        Sadece yer adlarını ve mümkünse semtlerini yaz, virgülle ayır.
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen turistik yer öneri botusun."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )

        text_response = response.choices[0].message.content.strip()
        spots = [
            spot.strip()
            for spot in re.split(r",|\n", text_response)
            if spot.strip() and len(spot.strip()) > 2
        ]
        return spots[:count]

    except Exception as e:
        print(f"Turistik yer öneri hatası: {e}")
        return []

def generate_multi_day_plan(start: str, end: str, stops: List[str], days: int) -> str:
    """
    Çok günlük gezi planı oluşturur.
    """
    try:
        stops_str = ', '.join(stops)
        prompt = f"""
        {days} günlük bir İstanbul gezi planı hazırla.
        Başlangıç noktası: {start}
        Bitiş noktası: {end}
        Arada ziyaret edilecek yerler: {stops_str}

        Günlere bölerek; her gün için rota, gezilecek yerler, yemek önerileri ve genel tavsiyeler ver.
        Çıktıyı Türkçe ve detaylı yaz.
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen profesyonel bir seyahat asistanısın."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"GPT Hatası: {e}")
        return f"{days} günlük gezi planı oluşturulamadı."
