import streamlit as st

st.title("🗺️ TripArchitect")
st.write("Seyahatinizi kişiselleştirin!")

city = st.text_input("Hangi şehre gidiyorsunuz?")
interests = st.text_input("İlgi alanlarınız (müze, restoran, tarihi yerler...)")
transport = st.selectbox("Ulaşım tercihiniz", ["Yürüyüş", "Araba", "Otobüs"])

if st.button("Rota Oluştur"):
    st.success(f"{city} için rota oluşturuluyor...")
