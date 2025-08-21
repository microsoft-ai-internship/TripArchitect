# 🗺️ TripArchitect — NLP-Based Travel Chatbot with AI Recommendations

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


<img width="1512" height="945" alt="Ekran Resmi 2025-08-21 17 55 18" src="https://github.com/user-attachments/assets/bea7283c-debb-407d-9c4f-6370c7c772c2" />
<img width="1512" height="945" alt="Ekran Resmi 2025-08-21 17 53 09" src="https://github.com/user-attachments/assets/667ba319-2baf-4930-b9cf-ef89766d3f80" />
<img width="1512" height="945" alt="Ekran Resmi 2025-08-21 17 53 18" src="https://github.com/user-attachments/assets/db2bff79-3bc0-4d6c-8ac1-1500ea120027" />
<img width="1512" height="945" alt="Ekran Resmi 2025-08-21 17 54 14" src="https://github.com/user-attachments/assets/ecc19871-092e-4a80-ba53-e319fb43751d" />
<img width="1512" height="945" alt="Ekran Resmi 2025-08-21 17 54 21" src="https://github.com/user-attachments/assets/28769596-eccb-4667-9239-58acc1d6a554" />
<img width="1512" height="945" alt="Ekran Resmi 2025-08-21 17 54 25" src="https://github.com/user-attachments/assets/7984e893-3776-438c-b45d-74d6ceb7c05a" />


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
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── profile.html
│   ├── css/
│   │   ├── login.css          
│   │   ├── auth.css          
│   │   ├── profile.css       
│   │   └── main.css          
│   ├── js/
│   │   ├── login.js          
│   │   ├── auth.js           
│   │   ├── profile.js         
│   │   └── main.js                               
│   └── venv/
└── README.md                  
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













