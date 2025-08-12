# backend/gpt_summarizer.py
import os
import json
import openai
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")
if not OPENAI_KEY:
    raise RuntimeError("OPENAI_KEY environment variable is missing.")
openai.api_key = OPENAI_KEY

# --------- Önemli: prompt'lar - ihtiyaç halinde ince ayar yapabilirsin ----------
STRUCTURE_PROMPT_INSTRUCTIONS = """
Aşağıdaki metni dikkatle analiz et. Kullanıcının doğal dilde verdiği isteği (ör. "3 günlük Kapadokya... Nilüfer'den Mudanya'ya...") parse et.
Çıktı **sadece** geçerli JSON olmalıdır (başka açıklama yok). Şu anahtarları içermelidir:

{
  "days": <integer veya null>,
  "start_location": "<string veya null>",
  "end_location": "<string veya null>",
  "budget": "<string ya da null>",         // eğer belirtilmişse
  "stops": [                               // her bir eleman bir günün duraklarıdır (array of arrays)
     ["Durak 1", "Durak 2", ...],         // 1. gün
     ["Durak 1", "Durak 2", ...]          // 2. gün
  ],
  "notes": "<kısa not (opsiyonel)>"
}

Kurallar:
- Eğer kullanıcı gün sayısı yazdıysa days integer olarak ver; yazmadıysa null.
- start_location / end_location yoksa null bırak.
- stops: mümkünse kullanıcının isteğine sadık kal; eğer kullanıcı özel durak yazdıysa onları kullan; yazmadıysa, mantıklı ve coğrafi açıdan uygun duraklar öner.
- Her gün için 4-6 durak olacak şekilde düzenle (kullanıcı istedi ise onun sayısına öncelik ver).
- JSON formatı strict olmalı (çift tırnak, geçerli JSON).
"""

def parse_user_text_to_structure(user_text: str) -> Dict:
    """
    Kullanıcının serbest metnini alır ve yukarıdaki JSON yapısını döndürür.
    Bu fonksiyon OpenAI çağrısı yapar.
    """
    prompt = STRUCTURE_PROMPT_INSTRUCTIONS + "\n\nKullanıcı İsteği:\n" + user_text

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sen yüksek kaliteli yapılandırılmış JSON üreten bir parselersin."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.25,
            max_tokens=800
        )
        txt = resp.choices[0].message.content.strip()

        # Eğer model bir açıklama ile JSON gönderirse, JSON kısmını ayıkla
        # Basit bir yöntem: ilk '{' den başlayıp son '}' ye kadar al
        first = txt.find("{")
        last = txt.rfind("}")
        if first != -1 and last != -1 and last > first:
            json_text = txt[first:last+1]
        else:
            json_text = txt

        data = json.loads(json_text)
        # Normalizasyon: eksik alanları ekle
        data.setdefault("days", data.get("days", None))
        data.setdefault("start_location", data.get("start_location", None))
        data.setdefault("end_location", data.get("end_location", None))
        data.setdefault("budget", data.get("budget", None))
        data.setdefault("stops", data.get("stops", []))
        data.setdefault("notes", data.get("notes", ""))

        return data

    except Exception as e:
        # Hata durumunda minimal fallback
        print(f"[gpt_summarizer.parse_user_text_to_structure] Hata: {e}")
        return {
            "days": None,
            "start_location": None,
            "end_location": None,
            "budget": None,
            "stops": [],
            "notes": ""
        }

def generate_place_descriptions(place_names: List[str]) -> Dict[str, str]:
    """
    Her bir mekan için 2-4 cümlelik kısa açıklama üretir.
    Dönen dict: { "Yer Adı": "Açıklama", ... }
    """
    if not place_names:
        return {}

    # prompt: bir liste halinde tüm isimleri ver ve kısa açıklama üretmesini iste
    joined = "\n".join(f"- {p}" for p in place_names)
    prompt = f"""
Aşağıdaki yerlerin her biri için 2 ila 4 cümlelik, seyahat eden bir kullanıcıya yönelik kısa açıklama yaz. 
Her açıklama 2-4 cümle olmalı; içerikte yerin ne olduğu, neden ziyaret edilebilir ve yaklaşık önerilen süre (örneğin 30-60 dk) belirt.
Çıktıyı JSON formatında ver: {{ "Yer Adı": "Açıklama", ... }}

Yerler:
{joined}
    """

    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Kısa ve faydalı gezi açıklamaları üret."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=800
        )
        txt = resp.choices[0].message.content.strip()
        # JSON ayıklama
        first = txt.find("{")
        last = txt.rfind("}")
        if first != -1 and last != -1 and last > first:
            json_text = txt[first:last+1]
        else:
            json_text = txt

        data = json.loads(json_text)
        return data
    except Exception as e:
        print(f"[gpt_summarizer.generate_place_descriptions] Hata: {e}")
        # fallback: basit açıklamalar
        return {p: f"{p} — bu yer hakkında kısa bilgi yok. (otomatik açıklama)" for p in place_names}