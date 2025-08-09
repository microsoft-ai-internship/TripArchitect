import streamlit as st
import sys
from pathlib import Path

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

# Proje kök yolunu ekleyelim (src klasörüne erişim için)
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent  # src klasörüne ulaşmak için
sys.path.append(str(project_root))

# Artık doğru import yapabiliriz
from src.chatbot.streamlit_app.chatbot_main import TripAssistantChatbot

# Sayfa ayarı
st.set_page_config(
    page_title="TripArchitect",
    layout="centered"
)

# Chat konteyneri
chat_container = st.container()

# Session state
if "chatbot" not in st.session_state:
    st.session_state.chatbot = TripAssistantChatbot(st.secrets["OPENAI_API_KEY"])
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesaj geçmişini göster
with chat_container:
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

# Kullanıcı girişi işleme
if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with chat_container:
        st.chat_message("user").write(prompt)

        with st.spinner("Rota oluşturuluyor..."):
            try:
                response = st.session_state.chatbot.get_chat_response(prompt)

                # Metin yanıtını göster
                st.chat_message("assistant").write(response["text_response"])

                # Harita verileri varsa işle
                if response.get("maps_data"):
                    md = response["maps_data"]

                    # Rota bilgileri
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.markdown(f"""
                        **🏁 Başlangıç:**  
                        {md['start_point']}  

                        **🏁 Bitiş:**  
                        {md['end_point']}
                        """)

                    with col2:
                        st.markdown(f"""
                        **⏱️ Tahmini Süre:**  
                        {int(md.get('duration', 0) / 60)} dakika  

                        **📏 Mesafe:**  
                        {int(md.get('distance', 0))} metre
                        """)

                    # Harita görüntüleme
                    st.divider()
                    st.components.v1.iframe(
                        md["embed_link"],
                        height=450,
                        scrolling=True
                    )

                    # Tam ekran butonu
                    st.link_button(
                        "🗺️ Google Maps'te Tam Ekran Aç",
                        md["direct_link"],
                        help=f"Başlangıç: {md['start_point']} → Bitiş: {md['end_point']}"
                    )

                    # Durak listesi
                    with st.expander("📌 Tüm Duraklar (Optimize Sıralama)"):
                        for i, loc in enumerate(md["optimized_route"], 1):
                            st.markdown(f"{i}. {loc}")

                    st.divider()

                # Mesaj geçmişine ekle
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["text_response"]
                })

            except Exception as e:
                st.error(f"Rota oluşturulurken hata oluştu: {str(e)}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin."
                })