import openai
from typing import List
import re


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
            temperature=0.3,  # Daha tutarlı sonuçlar için
            max_tokens=100
        )

        # Çıktıyı temizleme
        text_response = response.choices[0].message.content.strip()
        locations = [
            loc.strip()
            for loc in re.split(r",|\n", text_response)
            if loc.strip() and len(loc.strip()) > 2  # Tek harfli/kısaltmaları filtrele
        ]

        return locations[:6]  # En fazla 6 lokasyon dön

    except Exception as e:
        print(f"NLP Hatası: {e}")
        return []  # Fallback: Boş liste dön