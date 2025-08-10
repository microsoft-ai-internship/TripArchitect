import os
import openai
from dotenv import load_dotenv
from typing import List

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_KEY")
if not OPENAI_KEY:
    raise RuntimeError("OPENAI_KEY environment variable is missing.")
openai.api_key = OPENAI_KEY

def extract_locations(text: str) -> List[str]:
    """
    Kullanıcının metninden yer isimlerini GPT ile çıkarır.
    """
    prompt = f"""
    Aşağıdaki metinde geçen tüm şehir, ilçe, mahalle isimlerini Türkçe olarak listele. Sadece isimleri, virgül ile ayrılmış olarak yaz:

    {text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system", "content":"Sen bir dil işlem uzmanısın."},
            {"role":"user", "content": prompt}
        ],
        temperature=0,
        max_tokens=100
    )

    text_response = response.choices[0].message.content.strip()
    # Virgül ve yeni satıra göre ayır
    locations = [loc.strip() for loc in text_response.replace("\n",",").split(",") if loc.strip()]
    return locations
