import streamlit as st
import requests
from datetime import datetime
import pytz
import urllib.parse

# --- 1. SAYFA VE İKON YAPILANDIRMASI ---
st.set_page_config(
    page_title="Eczane Pro", 
    page_icon="icon.png", 
    layout="centered"
)

# --- 2. API ANAHTARI (Burayı Kontrol Et) ---
API_KEY = "apikey 0dioS4p4XYI5k184fEWJgv:3Z4WWAqncvGBtJFoPreWVY" 

# --- 3. MODERN TASARIM VE APPLE DESTEĞİ (CSS & HTML) ---
st.markdown("""
    <style>
    .stApp { background-color: #0d0d0d; color: #e0e0e0; }
    
    /* Eczane Kartı */
    .pro-card {
        background: #181818;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border-left: 5px solid #800020;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    .title-text { color: #ffffff; font-size: 22px; font-weight: 700; margin-bottom: 10px; }
    .info-text { color: #b0b0b0; font-size: 14px; margin-bottom: 5px; }
    
    /* Butonlar */
    .btn-container { display: flex; gap: 10px; margin-top: 15px; }
    
    .btn-custom {
        flex: 1;
        text-align: center;
        padding: 12px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        font-size: 14px;
        color: white !important;
        transition: 0.3s;
    }
    
    .bg-green { background-color: #1b4332; border: 1px solid #2d6a4f; }
    .bg-red { background-color: #432818; border: 1px solid #603808; }
    .bg-blue { background-color: #1a3a4a; border: 1px solid #2a5a7a; }
    
    /* Alt Bilgi İmzası */
    .footer {
        position: fixed;
        bottom: 10px;
        right: 20px;
        font-size: 12px;
        color: #555;
        text-align: right;
        background: rgba(13, 13, 13, 0.8);
        padding: 5px;
        border-radius: 5px;
        z-index: 1000;
    }
    </style>
""", unsafe_allow_html=True)

# Apple Cihazlar İçin Ana Ekran İkonu Zorlaması
st.markdown('<link rel="apple-touch-icon" href="https://raw.githubusercontent.com/mirbedirhanonverdi/mobil_eczane/main/icon.png">', unsafe_allow_html=True)

# --- 4. SAAT VE İMZA HESAPLAMA ---
try:
    tr_tz = pytz.timezone('Europe/Istanbul')
    zaman = datetime.now(tr_tz).strftime("%H:%M | %d.%m.%Y")
except:
    zaman = "Saat Alınamadı"

st.markdown(f"""<div class="footer">{zaman}<br><b>Mir Bedirhan Önverdi</b></div>""", unsafe_allow_html=True)

# --- 5. FONKSİYONLAR (HATA KORUMALI) ---
def veri_getir(endpoint, params):
    url = f"https://api.collectapi.com/health/{endpoint}"
    headers = {
        'authorization': f"apikey {API_KEY}",
        'content-type': "application/json"
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "msg": f"Hata Kodu: {response.status_code}"}
    except Exception as e:
        return {"success": False, "msg": "Bağlantı Hatası Gerçekleşti"}

# --- 6. ARAYÜZ ---
st.markdown("<h1 style='text-align: center; color: white;'>🏥 ECZANE PRO</h1>", unsafe_allow_html=True)

iller = ["Adana", "Adıyaman", "Afyon", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "İçel", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]
iller.sort()

col1, col2 = st.columns(2)
with col1:
    secilen_il = st.selectbox("Şehir Seçin", iller)

# İlçe listesini güvenli bir şekilde çekelim
dist_res = veri_getir("districtList", {"il": secilen_il})
ilceler = []
if dist_res.get("success"):
    ilceler = [d["text"] for d in dist_res["result"]]

with col2:
    secilen_ilce = st.selectbox("İlçe Seçin", ["Tümü"] + ilceler)

if st.button("🔍 Nöbetçi Eczaneleri Sorgula", use_container_width=True):
    p = {"il": secilen_il}
    if secilen_ilce != "Tümü":
        p["ilce"] = secilen_ilce
    
    with st.spinner("Güncel veriler alınıyor..."):
        res = veri_getir("dutyPharmacy", p)
        if res.get("success"):
            if not res["result"]:
                st.warning("Bu bölgede şu an kayıtlı nöbetçi eczane bulunamadı.")
            else:
                for e in res["result"]:
                    # Telefonu temizle
                    tel = e['phone'].replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
                    # Paylaşım linki
                    mesaj = f"{e['name']} Nöbetçi Eczanesi\n📍 {e['address']}\n📞 {e['phone']}"
                    wp_link = f"https://wa.me/?text={urllib.parse.quote(mesaj)}"
                    
                    st.markdown(f"""
                    <div class="pro-card">
                        <div class="title-text">{e['name']}</div>
                        <div class="info-text"><b>İlçe:</b> {e['dist']}</div>
                        <div class="info-text"><b>Adres:</b> {e['address']}</div>
                        <div class="info-text"><b>Telefon:</b> {e['phone']}</div>
                        <div class="btn-container">
                            <a href="tel:{tel}" class="btn-custom bg-green">📞 Ara</a>
                            <a href="http://maps.google.com/?q={e['name']}+{e['address']}" target="_blank" class="btn-custom bg-red">🗺️ Yol Tarifi</a>
                            <a href="{wp_link}" target="_blank" class="btn-custom bg-blue">💬 Paylaş</a>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error(f"Bir hata oluştu: {res.get('msg', 'Bilinmeyen Hata')}")
