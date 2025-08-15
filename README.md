# 🗺️ TripArchitect — AI-Powered Smart Route Planner

**TripArchitect**, is a route planning application that integrates artificial intelligence and mapping services, allowing users to create travel itineraries through free-text input.
By simply entering a request such as “A 1-day, 5-stop tour in Beşiktaş,” the user receives a professional route suggestion that includes map links, day-by-day plans, and detailed place descriptions.


## ✨ Features

- 🧠 **AI-Based Planning:** Generates routes and itineraries tailored to the user’s request via the OpenAI API  
- 🗺️ **Google Maps Integration:** Dynamic maps and location suggestions  
- 📍 **Location-Specific Filtering:** Suggestions restricted to the specified city/district (optional feature)  
- 📚 **Place Descriptions:** Short introduction text for each stop  
- 💾 **Chat History:** Easy access to previous itineraries  
- 🌙 **Dark/Light Theme Support**  
- 📱 **Responsive Design:** Modern interface compatible with both mobile and desktop devices  


## 🖼️ Sample Screenshots

<img width="1512" height="945" alt="Screenshot 2025-08-13 15 53 47" src="https://github.com/user-attachments/assets/817625cd-aadc-4334-843c-037cd5976f80" />
<img width="1512" height="864" alt="Screenshot 2025-08-13 16 19 39" src="https://github.com/user-attachments/assets/090bbcf9-ffe1-4100-b976-782d67bd7a67" />
<img width="1512" height="864" alt="Screenshot 2025-08-13 16 19 46" src="https://github.com/user-attachments/assets/39ee5158-69d9-4dc2-9f26-599f3a3fe62d" />
<img width="1512" height="864" alt="Screenshot 2025-08-13 16 19 48" src="https://github.com/user-attachments/assets/72ea4e53-f401-4323-b633-ae5877678fca" />


## 🛠️ Tech Stack

**Frontend:**
- HTML5, CSS3, JavaScript (Vanilla)  
- Responsive and modern UI design  

**Backend:**
- Python 3.11+  
- FastAPI  
- OpenAI API (GPT)  
- Google Maps API  

**Others:**
- dotenv (for secure API key management)  
- Uvicorn (ASGI server)  


## 📂 Project Structure

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

⚙️ Setup

1. **Clone the project:**

```bash
git clone https://github.com/username/TripArchitect.git
cd TripArchitect/backend
```

2. **Create a Python virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Create a .env file (inside the backend folder):**

```env
OPENAI_KEY=sk-xxxxxxxxxxxxxxxx
GOOGLE_MAPS_API_KEY=AIzaSyXXXXXX
```

5. **Run the backend:**

```bash
uvicorn main:app --reload
```

6. **Open the frontend:**
   Open `frontend/index.html`in your browser.


## 📌 Usage

1. Enter your travel plan into the chat box.
   **Example:**

```bash
2-day Istanbul trip, historical landmarks and a seaside dinner
```

2. TripArchitect will provide you with:

* A dynamic Google Map
* A day-by-day itinerary
* A pleasant description for each stop


## 🚀 Future Enhancements

* ✅ Ensure 100% accurate regional filtering
* 📷 Add location photos via Google Places API
* 🗣️ Voice assistant integration
* 📱 Progressive Web App (PWA) support
* 🌍 Multi-language interface













