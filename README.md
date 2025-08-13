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
<img width="1512" height="864" alt="Ekran Resmi 2025-08-13 16 19 39" src="https://github.com/user-attachments/assets/090bbcf9-ffe1-4100-b976-782d67bd7a67" />
<img width="1512" height="864" alt="Ekran Resmi 2025-08-13 16 19 46" src="https://github.com/user-attachments/assets/39ee5158-69d9-4dc2-9f26-599f3a3fe62d" />
<img width="1512" height="864" alt="Ekran Resmi 2025-08-13 16 19 48" src="https://github.com/user-attachments/assets/72ea4e53-f401-4323-b633-ae5877678fca" />

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
```

⚙️ Kurulum

1. **Projeyi klonlayın:**

```bash
git clone https://github.com/kullaniciadi/TripArchitect.git
cd TripArchitect/backend
```

2. **Python sanal ortamı oluşturun:**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Gerekli paketleri yükleyin:**

```bash
pip install -r requirements.txt
```

4. **`.env` dosyasını oluşturun (backend klasörü içine):**

```env
OPENAI_KEY=sk-xxxxxxxxxxxxxxxx
GOOGLE_MAPS_API_KEY=AIzaSyXXXXXX
```

5. **Backend’i çalıştırın:**

```bash
uvicorn main:app --reload
```

6. **Frontend’i açın:**
   `frontend/index.html` dosyasını tarayıcıda açın.

---

## 📌 Kullanım

1. Sohbet kutusuna seyahat planınızı yazın.
   **Örnek:**

```bash
2 günlük İstanbul gezisi, tarihi mekanlar ve deniz kenarında bir akşam yemeği
```

2. TripArchitect size:

* Dinamik Google Haritası
* Günlere ayrılmış rota listesi
* Her durak için güzel açıklama
  sunar.

---

## 🚀 Gelecek Geliştirmeler

* ✅ Bölgesel filtrelemeyi %100 kesin hale getirme
* 📷 Mekan fotoğraflarını Google Places API ile ekleme
* 🗣️ Sesli asistan entegrasyonu
* 📱 Progressive Web App (PWA) desteği
* 🌍 Çok dilli arayüz

---

## 📄 Lisans

Bu proje **MIT lisansı** altında sunulmaktadır.

````










