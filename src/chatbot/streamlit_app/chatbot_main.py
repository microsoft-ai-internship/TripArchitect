import openai
from typing import List, Dict, Optional
from urllib.parse import quote
import re
import json
from pathlib import Path
import sys

# Proje kök yolunu ekleyelim
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent  # src klasörüne ulaşmak için
sys.path.append(str(project_root))

# Artık absolute import kullanabiliriz
from src.chatbot.maps.route_api import GoogleMapsRouteAPI
from src.chatbot.maps.link_generator import GoogleMapsLinkGenerator
from src.chatbot.nlp.location_parser import extract_locations


class TripAssistantChatbot:
    def __init__(self, openai_api_key: str):
        openai.api_key = openai_api_key
        self.route_api = GoogleMapsRouteAPI()
        self.link_gen = GoogleMapsLinkGenerator()
        self.conversation_history = [
            {
                "role": "system",
                "content": """Profesyonel seyahat asistanısınız. Adımlar:
1. Kullanıcıdan şu bilgileri topla:
   - Şehir, tarih, ilgi alanları
   - Ulaşım tercihi (yürüme/araç)
   - Başlangıç noktası

2. Her gün için optimize rota oluştur:
   - Sabah/öğlen/akşam zaman dilimleri
   - Coğrafi sıralama yap
   - Dinlenme molaları ekle

3. Çıktı formatı:
   **Gün X: [Tarih] - [Bölge]**
   🕘 09:00: [Durak 1]
   🕙 11:00: [Durak 2]
   🗺️ Google Maps Linki: [Durak1], [Durak2], [Durak3]"""
            }
        ]

    def extract_trip_details(self, text: str) -> Dict[str, str]:
        """Metinden seyahat detaylarını çıkarır"""
        prompt = f"""Aşağıdaki mesajdaki seyahat detaylarını çıkar:
{text}

Çıktı formatı:
Şehir: 
Süre: 
İlgi Alanları: 
Ulaşım: 
Başlangıç Noktası:"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return self._parse_details(response.choices[0].message['content'])

    def _parse_details(self, text: str) -> Dict[str, str]:
        """Ham metni yapılandırılmış veriye çevirir"""
        details = {}
        for line in text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                details[key.strip()] = value.strip()
        return details

    def _process_locations(self, location_text: str) -> Optional[Dict]:
        """Lokasyon metnini işleyip harita verisi oluşturur"""
        locations = extract_locations(location_text)
        if len(locations) < 2:
            return None

        try:
            # Rota optimizasyonu
            optimized = self.route_api.get_optimized_route(locations)
            if not optimized:
                optimized_locations = locations
            else:
                optimized_locations = optimized['waypoints']

            # Link oluşturma
            return {
                'direct_link': self.link_gen.generate_direct_link(optimized_locations),
                'embed_link': self.link_gen.generate_embed_link(optimized_locations),
                'optimized_route': optimized_locations,
                'start_point': optimized_locations[0],
                'end_point': optimized_locations[-1],
                'duration': optimized.get('duration', 0),
                'distance': optimized.get('distance', 0)
            }
        except Exception as e:
            print(f"Harita verisi oluşturma hatası: {e}")
            return None

    def generate_itinerary(self, details: Dict[str, str]) -> str:
        """Seyahat planı oluşturur"""
        prompt = f"""Aşağıdaki detaylara göre detaylı seyahat planı oluştur:
{json.dumps(details, indent=2)}

Önemli Kurallar:
1. Her gün için coğrafi olarak optimize edilmiş rota
2. Her aktivite için gerçekçi zaman aralıkları
3. Son satırda tüm durakları virgülle ayırarak belirt:
Google Maps Linki: [Durak1], [Durak2], [Durak3]"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5
        )
        return response.choices[0].message['content']

    def get_chat_response(self, user_input: str) -> Dict:
        """Kullanıcı mesajını işler ve tam yanıt döner"""
        self.conversation_history.append({"role": "user", "content": user_input})

        # 1. Seyahat detaylarını çıkar
        trip_details = self.extract_trip_details(user_input)

        # 2. Plan oluştur
        itinerary = self.generate_itinerary(trip_details)

        # 3. Harita verilerini oluştur
        maps_data = None
        if 'Google Maps Linki:' in itinerary:
            location_text = itinerary.split('Google Maps Linki:')[1].strip()
            maps_data = self._process_locations(location_text)

        # 4. Yanıtı formatla
        return {
            "text_response": itinerary.split('Google Maps Linki:')[0].strip(),
            "maps_data": maps_data,
            "trip_details": trip_details
        }