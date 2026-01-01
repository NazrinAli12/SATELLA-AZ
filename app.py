import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io
from PIL import Image

# 1. Səhifə Konfiqurasiyası
st.set_page_config(page_title="SATELLA AI", layout="wide", initial_sidebar_state="expanded")

# 2. UI Təkmilləşdirməsi (Sidebar-ı stabil saxlayan CSS)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .main { background-color: #0b0d0e !important; font-family: 'Inter', sans-serif; }
    
    /* Sidebar-ı stabil saxla və itməsinə imkan vermə */
    [data-testid="stSidebar"] {
        min-width: 380px !important;
        background-color: #0d1117 !important;
        border-right: 1px solid #30363d !important;
    }

    [data-testid="stHeader"] { display: none !important; }

    .brand-card {
        background: linear-gradient(135deg, #1f6feb 0%, #111827 100%);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
</style>
""", unsafe_allow_html=True)

# 3. Köməkçi Funksiyalar
def process_images(img1, img2):
    i1 = Image.open(img1)
    i2 = Image.open(img2)
    return i1.resize((800, 600)), i2.resize((800, 600))

# --- SOL SIDEBAR ---
with st.sidebar:
    st.markdown("""<div class="brand-card"><h2 style='color:white;margin:0;'>🛰️ SATELLA AI</h2></div>""", unsafe_allow_html=True)
    
    st.markdown("### 📍 Koordinatlar")
    lat_val = st.text_input("Latitude", value="40.394799")
    lon_val = st.text_input("Longitude", value="49.849585")
    
    st.markdown("### 🛰️ Şəkillər")
    t0_file = st.file_uploader("Referans (T0)", type=["png","jpg"])
    t1_file = st.file_uploader("Cari (T1)", type=["png","jpg"])
    
    if st.button("🚀 ANALİZİ BAŞLAT", use_container_width=True):
        if t0_file and t1_file:
            st.session_state.lat = float(lat_val)
            st.session_state.lon = float(lon_val)
            st.session_state.run = True

# --- ƏSAS EKRAN ---
lat = st.session_state.get('lat', 40.394799)
lon = st.session_state.get('lon', 49.849585)

# Xəritə (Burada artıq xəta olmayacaq)
m = folium.Map(location=[lat, lon], zoom_start=18)
folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri",
    name="Esri World Imagery"
).add_to(m)
folium.Marker([lat, lon]).add_to(m)

folium_static(m, width=1100, height=550)

if t0_file and t1_file:
    img1, img2 = process_images(t0_file, t1_file)
    c1, c2 = st.columns(2)
    c1.image(img1, caption="Baseline")
    c2.image(img2, caption="Current")
