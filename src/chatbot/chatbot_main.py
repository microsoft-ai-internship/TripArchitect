def get_user_preferences():
    print("Merhaba! Hangi şehri ziyaret edeceksiniz?")
    city = input("Şehir: ")

    print("Nasıl bir rota istersiniz? (tarihi yerler, restoranlar, müzeler...)")
    interests = input("İlgi alanları: ")

    print("Nasıl ulaşım tercih edersiniz? (yürüyüş, araba, otobüs)")
    transport = input("Ulaşım türü: ")

    return {
        "city": city,
        "interests": interests,
        "transport": transport
    }

if __name__ == "__main__":
    prefs = get_user_preferences()
    print("\n📍 Tercihleriniz alındı:")
    print(prefs)
