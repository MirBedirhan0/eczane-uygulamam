import streamlit as st
import requests
from datetime import datetime

# --- YAPILANDIRMA ---
# Buraya CollectAPI'den aldığın API Key'i yapıştır
API_KEY = "apikey 0dioS4p4XYI5k184fEWJgv:3Z4WWAqncvGBtJFoPreWVY" 

# 1. Sayfa Ayarları ve Tema
st.set_page_config(page_title="Eczane Pro", page_icon="💊", layout="centered")

st.markdown("""
    <style>
    /* Antrasit / Gri-Siyah Tema */
    .stApp {
        background-color: #121212;
        color: #cfcfcf;
    }
    /* Kart Tasarımları */
    .eczane-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #800020;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .eczane-baslik { color: #ffffff; font-size: 20px; font-weight: bold; }
    .eczane-detay { color: #aaaaaa; font-size: 14px; margin-top: 5px; }
    
    /* Sağ Alt İmza ve Saat */
    .fixed-footer {
        position: fixed;
        bottom: 15px;
        right: 20px;
        text-align: right;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 13px;
        color: #666666;
        background: rgba(18, 18, 18, 0.8);
        padding: 5px 10px;
        border-radius: 8px;
        z-index: 1000;
    }
    /* Input ve Selectbox düzenlemeleri */
    div[data-baseweb="select"] > div {
        background-color: #262626 !important;
        border: 1px solid #333 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Yardımcı Fonksiyonlar (API Bağlantısı)
def veri_cek(endpoint, params={}):
    headers = {
        'authorization': f"apikey {API_KEY}",
        'content-type': "application/json"
    }
    url = f"https://api.collectapi.com/health/{endpoint}"
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    return None

# 3. Sidebar / Sabit İmza Alanı
simdi = datetime.now().strftime("%d.%m.%Y | %H:%M")
st.markdown(f"""
    <div class="fixed-footer">
        {simdi}<br>
        <b>Mir Bedirhan Önverdi</b>
    </div>
""", unsafe_allow_html=True)

# 4. Ana Uygulama Arayüzü
st.title("🏥 Nöbetçi Eczane Sistemi")

# Şehir Listesi
iller = ["Adana", "Adıyaman", "Afyon", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "İçel", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]
iller.sort()

col1, col2 = st.columns(2)

with col1:
    secilen_il = st.selectbox("Şehir Seçin:", iller)

# Dinamik İlçe Getirme
ilce_listesi = []
with st.spinner("İlçeler yükleniyor..."):
    res_ilce = veri_cek("districtList", {"il": secilen_il})
    if res_ilce and res_ilce.get("success"):
        ilce_listesi = [i["text"] for i in res_ilce["result"]]

with col2:
    secilen_ilce = st.selectbox("İlçe Seçin (Opsiyonel):", ["Tümü"] + ilce_listesi)

if st.button("Eczaneleri Sorgula", use_container_width=True):
    params = {"il": secilen_il}
    if secilen_ilce != "Tümü":
        params["ilce"] = secilen_ilce
        
    with st.status("Veriler güncelleniyor...", expanded=False) as status:
        data = veri_cek("dutyPharmacy", params)
        if data and data.get("success"):
            status.update(label="Eczaneler başarıyla getirildi!", state="complete")
            
            for eczane in data["result"]:
                st.markdown(f"""
                    <div class="eczane-card">
                        <div class="eczane-baslik">{eczane['name']}</div>
                        <div class="eczane-detay">📍 <b>İlçe:</b> {eczane['dist']}</div>
                        <div class="eczane-detay">🏠 <b>Adres:</b> {eczane['address']}</div>
                        <div class="eczane-detay">📞 <b>Telefon:</b> {eczane['phone']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Konum butonu (Google Maps linki)
                lat_lng = eczane['loc']
                st.write(f"[🗺️ Haritada Göster](https://www.google.com/maps/search/?api=1&query={lat_lng})")
        else:
            status.update(label="Bir hata oluştu veya bu bölgede kayıt bulunamadı.", state="error")