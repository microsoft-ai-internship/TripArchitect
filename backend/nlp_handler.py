import re
from typing import Dict, Any


def extract_intent(text: str) -> Dict[str, Any]:
    """Basit regex tabanlı intent çıkarımı"""
    # Bütçe çıkarımı
    budget = re.findall(r"(\d+)\s*-\s*(\d+)\s*TL", text)

    # Süre çıkarımı
    duration = re.search(r"(\d+)\s*gün|lük", text)

    # Kategoriler
    categories = []
    if re.search(r"tarihi|müze|saray", text, re.IGNORECASE):
        categories.append("museum")
    if re.search(r"modern|alışveriş|avm", text, re.IGNORECASE):
        categories.append("shopping_mall")

    return {
        "budget": (int(budget[0][0]), int(budget[0][1])) if budget else (3000, 5000),
        "duration": int(duration.group(1)) if duration else 1,
        "location": "Beşiktaş" if "Beşiktaş" in text else "İstanbul",
        "categories": categories if categories else ["tourist_attraction"]
    }