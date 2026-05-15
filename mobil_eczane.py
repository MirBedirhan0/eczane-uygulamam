import streamlit as st
import requests
from datetime import datetime
import pytz

# --- AYARLAR ---
API_KEY = "apikey 0dioS4p4XYI5k184fEWJgv:3Z4WWAqncvGBtJFoPreWVY" # CollectAPI Key'ini buraya yaz

st.set_page_config(page_title="Eczane Pro v2", page_icon="💊", layout="centered")

# --- GELİŞMİŞ TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0f0f0f; color: #e0e0e0; }
    
    /* Eczane Kartı */
    .pro-card {
        background: linear-gradient(145deg, #1a1a1a, #121212);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #333;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
    }
    
    .title-text { color: #ffffff; font-size: 22px; font-weight: 800; margin-bottom: 10px; }
    .info-text { color: #b0b0b0; font-size: 14px; margin-bottom: 5px; display: flex; align-items: center; }
    
    /* Profesyonel Butonlar */
    .button-container { display: flex; gap: 10px; margin-top: 15px; }
    
    .btn {
        flex: 1;
        text-align: center;
        padding: 10px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: bold;
        font-size: 14px;
        transition: 0.3s;
    }
    
    .btn-call { background-color: #1e3a2f; color: #4ade80; border: 1px solid #4ade80; }
    .btn-map { background-color: #3b1e1e; color: #fb7185; border: 1px solid #fb7185; }
    
    /* İmza Alanı */
    .footer {
        position: fixed;
        bottom: 10px;
        right: 15px;
        font-size: 11px;
        color: #555;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

# --- SAAT VE İMZA ---
tr_tz = pytz.timezone('Europe/Istanbul')
current_time = datetime.now(tr_tz).strftime("%H:%M | %d.%m.%Y")

st.markdown(f"""<div class="footer">{current_time}<br><b>Mir Bedirhan Önverdi</b></div>""", unsafe_allow_html=True)

# --- BAŞLIK ---
st.markdown("<h1 style='text-align: center; color: white;'>💊 ECZANE PRO</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>81 İlde Anlık Nöbetçi Eczaneler</p>", unsafe_allow_html=True)

# --- VERİ ÇEKME ---
def get_data(endpoint, params):
    url = f"https://api.collectapi.com/health/{endpoint}"
    headers = {'authorization': f"apikey {API_KEY}", 'content-type': "application/json"}
    return requests.get(url, headers=headers, params=params).json()

# --- ŞEHİR SEÇİMİ ---
iller = ["Adana", "Adıyaman", "Afyon", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "İçel", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]
iller.sort()

c1, c2 = st.columns(2)
with c1:
    il = st.selectbox("Şehir", iller)
with c2:
    dist_data = get_data("districtList", {"il": il})
    ilceler = [d["text"] for d in dist_data["result"]] if dist_data.get("success") else []
    ilce = st.selectbox("İlçe (Tümü)", ["Tümü"] + ilceler)

if st.button("Eczaneleri Bul", use_container_width=True):
    query = {"il": il}
    if ilce != "Tümü": query["ilce"] = ilce
    
    with st.spinner("Veriler getiriliyor..."):
        res = get_data("dutyPharmacy", query)
        if res.get("success"):
            for e in res["result"]:
                # Telefon formatını temizle
                clean_phone = e['phone'].replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
                
                st.markdown(f"""
                <div class="pro-card">
                    <div class="title-text">🏥 {e['name']}</div>
                    <div class="info-text">📍 {e['dist']} / {e['address']}</div>
                    <div class="info-text">📞 {e['phone']}</div>
                    <div class="button-container">
                        <a href="tel:{clean_phone}" class="btn btn-call">📞 Hemen Ara</a>
                        <a href="https://www.google.com/maps/search/?api=1&query={e['name']}+{e['address']}" target="_blank" class="btn btn-map">🗺️ Yol Tarifi</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Bir sorun oluştu. Lütfen tekrar deneyin.")
