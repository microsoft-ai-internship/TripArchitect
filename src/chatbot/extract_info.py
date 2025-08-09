import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_trip_info_from_messages(messages):
    """
    messages: [{'role':..., 'content':...}, ...]
    OpenAI GPT ile mesajları analiz edip seyahat anahtar bilgilerini çıkarır.
    Döner: {
        "location": str,
        "days": str,
        "budget": str,
        "interests": [str],
        "transport": str
    }
    """

    prompt = """Aşağıdaki sohbetten seyahat planı ile ilgili bilgileri çıkar. JSON olarak dön.
    Anahtarlar: location, days, budget, interests (liste), transport.
    Eğer bilgi yoksa boş bırak.
    Sohbet:
    """

    # Sohbet metnine dönüştür
    chat_text = "\n".join([f"{m['role']}: {m['content']}" for m in messages])

    full_prompt = prompt + chat_text

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":full_prompt}],
        temperature=0,
        max_tokens=300,
    )
    text = response.choices[0].message['content'].strip()

    try:
        import json
        trip_info = json.loads(text)
    except Exception:
        trip_info = {}

    return trip_info
