# 🗺️ TripArchitect — AI Destekli Akıllı Rota Planlayıcı

**TripArchitect**, kullanıcıların serbest metin ile seyahat planları oluşturmasına imkân tanıyan, yapay zekâ ve harita servisleri ile entegre çalışan bir rota planlama uygulamasıdır.  
Kullanıcı, yalnızca “Beşiktaş’ta 1 günlük 5 duraklı gezi planı” gibi basit bir ifade girerek; harita bağlantıları, gün bazlı planlar ve mekan açıklamaları içeren profesyonel bir rota önerisi alır.

---

## ✨ Özellikler

- 🧠 **AI Tabanlı Planlama:** OpenAI API ile kullanıcı isteğine uygun rota ve plan oluşturma
- 🗺️ **Google Maps Entegrasyonu:** Dinamik harita ve konum önerileri
- 📍 **Bölgeye Özel Filtreleme:** Kullanıcının belirttiği şehir/ilçe dışına çıkmayan öneriler (isteğe bağlı geliştirme)
- 📚 **Mekan Açıklamaları:** Her durak için kısa tanıtım metinleri
- 💾 **Sohbet Geçmişi:** Önceki planlara kolay erişim
- 🌙 **Karanlık/aydınlık tema desteği**
- 📱 **Responsive Tasarım:** Mobil ve masaüstü uyumlu modern arayüz

---

## 🖼️ Örnek Ekran Görüntüleri

<img width="1512" height="945" alt="Ekran Resmi 2025-08-13 15 53 47" src="https://github.com/user-attachments/assets/817625cd-aadc-4334-843c-037cd5976f80" />

---

## 🛠️ Teknoloji Yığını

**Frontend:**
- HTML5, CSS3, JavaScript (Vanilla)
- Responsive ve modern UI tasarımı

**Backend:**
- Python 3.11+
- FastAPI
- OpenAI API (GPT)
- Google Maps API

**Diğer:**
- dotenv (API anahtarlarını güvenle yönetmek için)
- Uvicorn (ASGI sunucu)

---

## 📂 Proje Yapısı

```plaintext
TripArchitect/
├── backend/
│   ├── __init__.py
│   ├── __pycache__/
│   ├── google_maps.py
│   ├── gpt_summarizer.py
│   ├── main.py
│   ├── nlp_handler.py
│   ├── requirements.txt
│   ├── schemas.py
│   └── venv/
├── frontend/
│   ├── app.js
│   ├── index.html
│   ├── style.css
│   └── venv/

