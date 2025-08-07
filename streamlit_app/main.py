import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from streamlit_extras.colored_header import colored_header

# Sayfa ayarları
st.set_page_config(
    page_title="TripArchitect | Kişisel Seyahat Planlayıcı",
    page_icon="✈️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS enjeksiyonu
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
    }

    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }

    @media (max-width: 768px) {
        .main {
            padding: 1rem;
        }
        .stButton>button {
            padding: 10px 20px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Ana başlık
colored_header(
    label="✈️ TRIPARCHITECT",
    description="Seyahat deneyiminizi kişiselleştirin",
    color_name="blue-70"
)

# Form alanı
with stylable_container(
        key="input_form",
        css_styles="""
    {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }
    """
):
    # Şehir girişi
    city = st.text_input(
        "📍 **Hangi şehri keşfetmek istersiniz?**",
        placeholder="Örn: İstanbul, Paris, Tokyo...",
        key="city_input"
    )

    # İlgi alanları
    interests = st.multiselect(
        "✨ **Neleri görmek istersiniz?**",
        options=["Müzeler", "Tarihi Yerler", "Restoranlar",
                 "Doğa", "Alışveriş", "Eğlence"],
        default=["Müzeler", "Restoranlar"],
        key="interests_select"
    )

    # Ulaşım seçimi
    transport = st.radio(
        "🚗 **Nasıl gezeceksiniz?**",
        options=["Yürüyerek", "Araçla", "Toplu Taşıma"],
        horizontal=True,
        key="transport_radio"
    )

    # Buton
    if st.button(
            "**ROTA OLUŞTUR**",
            use_container_width=True,
            type="primary"
    ):
        with st.spinner("Sizin için en iyi rotayı hazırlıyoruz..."):
            # Simüle edilmiş yükleme efekti
            import time

            time.sleep(2)

            # Başarı mesajı
            st.toast(f"{city} rotası hazır!", icon="✅")

            # Sonuç kartı
            with stylable_container(
                    key="result_card",
                    css_styles="""
                {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border-radius: 16px;
                    padding: 2rem;
                    margin-top: 1rem;
                }
                """
            ):
                st.markdown(f"""
                ### 🗺️ {city} Seyahat Planı

                **Keşif Rotası:**  
                {" → ".join(["Tarihi Merkez", "Modern Sanat Müzesi", "Liman Restoranı"])}

                **Ulaşım:** {transport}  
                **Toplam Süre:** ~3 saat

                *"Bu şehirde en iyi deneyim için sabah erken başlamanızı öneririz."*
                """)

# Footer
st.markdown("---")
st.caption("© 2025 TripArchitect | AI Destekli Seyahat Planlama")