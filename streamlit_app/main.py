import streamlit as st
from streamlit_folium import folium_static
import folium
from datetime import datetime, timedelta
import googlemaps
from dotenv import load_dotenv
import os
import openai
import time
import json

# Çevresel değişkenler
load_dotenv()

# Sayfa ayarları
st.set_page_config(
    page_title="TripGenius | AI Seyahat Asistanı",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo',
        'Report a bug': "https://github.com/your-repo/issues",
        'About': "# AI Destekli Kişiselleştirilmiş Seyahat Planlayıcı"
    }
)

# API anahtarları
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Google Maps istemcisi
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY) if GOOGLE_MAPS_API_KEY else None
openai.api_key = OPENAI_API_KEY

# CSS enjeksiyonu
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

    :root {
        --primary: #4361ee;
        --secondary: #3a0ca3;
        --accent: #f72585;
        --light: #f8f9fa;
        --dark: #212529;
        --gray: #6c757d;
        --success: #4cc9f0;
    }

    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .main {
        background-color: #f8fafc;
    }

    .stChatInput {
        border-radius: 12px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    }

    .stChatMessage {
        padding: 1rem 1.5rem;
        border-radius: 18px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .user-message {
        background-color: var(--light) !important;
        border-left: 4px solid var(--primary) !important;
    }

    .assistant-message {
        background-color: white !important;
        border-left: 4px solid var(--success) !important;
    }

    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
        border-right: 1px solid #e9ecef;
    }

    .map-container {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        height: 600px;
    }

    .itinerary-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .itinerary-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
    }

    .itinerary-time {
        color: var(--primary);
        font-weight: 600;
    }

    .itinerary-location {
        font-weight: 600;
        margin: 0.25rem 0;
    }

    .itinerary-desc {
        color: var(--gray);
        font-size: 0.9rem;
    }

    .stMarkdown h2 {
        color: var(--primary) !important;
        margin-top: 1.5rem !important;
    }

    .stButton>button {
        background: linear-gradient(90deg, var(--primary) 0%, var(--secondary) 100%);
        border: none;
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(67, 97, 238, 0.3);
    }

    .tag {
        display: inline-block;
        background-color: #e9ecef;
        padding: 0.25rem 0.75rem;
        border-radius: 50px;
        font-size: 0.8rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        color: var(--dark);
    }

    .tag-primary {
        background-color: rgba(67, 97, 238, 0.1);
        color: var(--primary);
    }

    .tag-accent {
        background-color: rgba(247, 37, 133, 0.1);
        color: var(--accent);
    }

    @media (max-width: 768px) {
        .map-container {
            height: 400px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Oturum durumu başlatma
if 'messages' not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant",
         "content": "Merhaba! Ben TripGenius, kişisel seyahat asistanınız. 🌍\n\nNereyi keşfetmek istersiniz? Bana seyahat planlarınızdan bahsedin, size özel bir rota oluşturup harita üzerinde göstereyim!"}
    ]

if 'itinerary' not in st.session_state:
    st.session_state.itinerary = None

if 'map_data' not in st.session_state:
    st.session_state.map_data = None

if 'map_center' not in st.session_state:
    st.session_state.map_center = [41.0082, 28.9784]  # İstanbul varsayılan


# Yardımcı fonksiyonlar
def generate_itinerary_with_ai(prompt):
    """OpenAI kullanarak seyahat planı oluşturur"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """
                Sen bir seyahat asistanısın. Kullanıcıların tercihlerine göre detaylı seyahat planları oluşturmalarına yardım ediyorsun.
                Planlar şunları içermeli:
                1. Günlük program (zaman aralıklarıyla)
                2. Her aktivite için kısa açıklama
                3. Ulaşım önerileri
                4. Önemli ipuçları

                Yanıtlarını JSON formatında ver. Örnek format:
                {
                    "summary": "Genel plan özeti",
                    "days": [
                        {
                            "day": "Gün 1",
                            "date": "YYYY-MM-DD",
                            "activities": [
                                {
                                    "time": "09:00 - 10:30",
                                    "location": "Yer adı",
                                    "description": "Açıklama",
                                    "type": "müze/tarihi/restoran vb.",
                                    "coordinates": [lat, lng]
                                }
                            ]
                        }
                    ],
                    "transportation": "Ulaşım önerileri",
                    "tips": "Genel ipuçları"
                }
                """},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content
        # JSON verisini temizle
        if content.startswith("```json"):
            content = content[7:-3]  # ```json ve kapanış ```'ı kaldır

        return json.loads(content)
    except Exception as e:
        st.error(f"AI plan oluştururken hata: {str(e)}")
        return None


def get_coordinates(location_name, city="İstanbul"):
    """Google Maps API ile koordinatları al"""
    try:
        geocode_result = gmaps.geocode(f"{location_name}, {city}")
        if geocode_result:
            loc = geocode_result[0]['geometry']['location']
            return [loc['lat'], loc['lng']]
        return None
    except Exception as e:
        st.error(f"Koordinat alınırken hata: {str(e)}")
        return None


def create_map(itinerary_data):
    """Folium ile interaktif harita oluştur"""
    if not itinerary_data or not itinerary_data.get('days'):
        return None

    # Harita merkezini belirle (ilk aktivite)
    first_activity = itinerary_data['days'][0]['activities'][0]
    map_center = first_activity.get('coordinates', [41.0082, 28.9784])

    m = folium.Map(location=map_center, zoom_start=13, control_scale=True)

    # Tüm aktiviteleri haritaya ekle
    for day in itinerary_data['days']:
        for i, activity in enumerate(day['activities']):
            if not activity.get('coordinates'):
                continue

            # Marker ekle
            popup_content = f"""
            <div style="width: 200px;">
                <h4 style="margin: 0; color: #4361ee;">{activity['location']}</h4>
                <p style="margin: 5px 0; font-size: 0.9em; color: #555;">{activity['time']}</p>
                <p style="margin: 5px 0; font-size: 0.85em;">{activity['description']}</p>
            </div>
            """

            folium.Marker(
                location=activity['coordinates'],
                popup=folium.Popup(popup_content, max_width=250),
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)

            # Çizgi ekle (sonraki aktivite varsa)
            if i < len(day['activities']) - 1:
                next_activity = day['activities'][i + 1]
                if next_activity.get('coordinates'):
                    folium.PolyLine(
                        locations=[activity['coordinates'], next_activity['coordinates']],
                        color='#4361ee',
                        weight=3,
                        dash_array='5,5'
                    ).add_to(m)

    return m


def generate_google_maps_link(coordinates_list):
    """Google Maps linki oluştur"""
    if not coordinates_list:
        return ""

    base_url = "https://www.google.com/maps/dir/"
    coordinates_str = "/".join([f"{coord[0]},{coord[1]}" for coord in coordinates_list])
    return base_url + coordinates_str


# UI Düzeni
st.title("🌍 TripGenius - AI Seyahat Asistanı")
st.caption("Sohbet ederek kişiselleştirilmiş seyahat planları oluşturun")

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.subheader("Seyahat Planınız")

    if st.session_state.itinerary:
        with st.expander("📅 Plan Özeti", expanded=True):
            st.write(st.session_state.itinerary['summary'])

            for day in st.session_state.itinerary['days']:
                st.markdown(f"### {day['day']} - {day.get('date', '')}")

                for activity in day['activities']:
                    with st.container():
                        st.markdown(f"""
                        <div class="itinerary-card">
                            <div class="itinerary-time">{activity['time']}</div>
                            <div class="itinerary-location">{activity['location']}</div>
                            <div class="itinerary-desc">{activity['description']}</div>
                            <div style="margin-top: 0.5rem;">
                                <span class="tag tag-primary">{activity['type']}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

        st.markdown("### 🚗 Ulaşım Önerileri")
        st.info(st.session_state.itinerary.get('transportation', 'Ulaşım bilgisi yok'))

        st.markdown("### 💡 İpuçları")
        st.info(st.session_state.itinerary.get('tips', 'İpucu yok'))

        if st.session_state.itinerary.get('days') and st.session_state.itinerary['days'][0]['activities']:
            all_coords = [act['coordinates'] for day in st.session_state.itinerary['days']
                          for act in day['activities'] if act.get('coordinates')]

            if all_coords:
                maps_link = generate_google_maps_link(all_coords)
                st.markdown(f"""
                ### 📍 Harita Linki
                [Google Maps'te bu rotayı aç]({maps_link})
                """)
    else:
        st.info(
            "Henüz bir seyahat planı oluşturulmadı. Sağdaki sohbet panelinden bana seyahat planlarınızdan bahsedin!")

with col2:
    # Sohbet arayüzü
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🌍" if message["role"] == "assistant" else "👤"):
            st.markdown(message["content"])

    if prompt := st.chat_input("Seyahat planlarınızı yazın..."):
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant", avatar="🌍"):
            with st.spinner("Sizin için en iyi seyahat planını hazırlıyorum..."):
                # AI ile plan oluştur
                itinerary_data = generate_itinerary_with_ai(prompt)

                if itinerary_data:
                    # Koordinatları doldur (eğer yoksa)
                    for day in itinerary_data['days']:
                        for activity in day['activities']:
                            if not activity.get('coordinates'):
                                coords = get_coordinates(activity['location'])
                                if coords:
                                    activity['coordinates'] = coords

                    st.session_state.itinerary = itinerary_data
                    st.session_state.map_data = create_map(itinerary_data)

                    # Yanıt oluştur
                    response = f"""
                    **{itinerary_data['summary']}**

                    İşte sizin için hazırladığım detaylı seyahat planı:
                    """

                    for day in itinerary_data['days']:
                        response += f"\n\n### {day['day']}\n"
                        for activity in day['activities']:
                            response += f"- **{activity['time']}**: {activity['location']} - {activity['description']}\n"

                    response += f"\n\n**Ulaşım Önerileri**: {itinerary_data.get('transportation', '')}"
                    response += f"\n\n**İpuçları**: {itinerary_data.get('tips', '')}"

                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})

                    # Haritayı göster
                    if st.session_state.map_data:
                        st.markdown("### 🗺️ Seyahat Rotası")
                        with st.container():
                            folium_static(st.session_state.map_data, height=500)
                else:
                    error_msg = "Üzgünüm, seyahat planı oluştururken bir hata oluştu. Lütfen daha detaylı bilgi vererek tekrar deneyin."
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Sidebar
with st.sidebar:
    st.image("https://via.placeholder.com/300x80?text=TripGenius", use_column_width=True)
    st.markdown("""
    ### 🧭 Seyahat Tercihleriniz

    Sohbete başlamadan önce genel tercihlerinizi belirleyin:
    """)

    travel_style = st.selectbox(
        "Seyahat Tarzınız",
        ["Kültür & Tarih", "Doğa & Macera", "Yemek & Eğlence", "Alışveriş", "Dinlence"]
    )

    pace = st.select_slider(
        "Tempo",
        options=["Çok Yavaş", "Yavaş", "Orta", "Hızlı", "Çok Hızlı"],
        value="Orta"
    )

    budget = st.radio(
        "Bütçe",
        options=["💰 Ekonomik", "💰💰 Orta", "💰💰💰 Lüks"],
        horizontal=True
    )

    st.markdown("---")
    st.markdown("""
    ### ✨ Özellikler
    - Sohbet tabanlı seyahat planlama
    - Kişiselleştirilmiş rota önerileri
    - Gerçek zamanlı harita entegrasyonu
    - Google Maps bağlantısı
    """)

    st.markdown("---")
    st.caption("""
    Made with ❤️ by TripGenius Team  
    [Github Repo](https://github.com/your-repo) | [Feedback](mailto:feedback@tripgenius.com)
    """)