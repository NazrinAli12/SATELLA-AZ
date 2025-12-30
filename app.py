import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io

# 1. Səhifə Konfiqurasiyası
st.set_page_config(page_title="SATELLA AI", layout="wide", initial_sidebar_state="expanded")

# 2. UI Təkmilləşdirməsi (No-Scroll Sidebar + Sağ Panel)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Inter', sans-serif;
        background-color: #0b0d0e !important;
        overflow: hidden !important;
    }

    [data-testid="stHeader"] { display: none; }

    /* SOL SİDEBAR - Yığcam dizayn */
    section[data-testid="stSidebar"] {
        width: 360px !important;
        background-color: #111418 !important;
        border-right: 1px solid #2d333b !important;
    }
    section[data-testid="stSidebar"] > div {
        height: 100vh !important;
        overflow: hidden !important;
        padding: 1.2rem !important;
    }

    /* SAĞ PANEL */
    [data-testid="column"]:nth-child(2) {
        background-color: #111418 !important;
        border-left: 1px solid #2d333b !important;
        padding: 20px !important;
        height: 100vh;
    }

    /* Elementləri sıxmaq */
    .stVerticalBlock { gap: 0.4rem !important; }
    
    /* Düymə və Kartlar */
    div.stButton > button {
        background: #1a73e8 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        height: 40px !important;
        width: 100%;
    }
    .metric-box {
        background: #1a1f24;
        border: 1px solid #3c4043;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 3. PDF Funksiyası
def generate_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "SATELLA ANALYSIS REPORT", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Coordinates: {lat}, {lon}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- SOL SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1e3a8a,#3b82f6);padding:1rem;border-radius:10px;margin-bottom:1rem'>
        <h2 style='color:white;margin:0;font-size:20px;'>🛰️ SATELLA</h2>
        <p style='color:#bfdbfe;margin:0;font-size:11px'>Enterprise AI Monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-size:11px; font-weight:700; color:#9ca3af;'>COORDINATES</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: lat_val = st.text_input("Lat", value="40.461023", label_visibility="collapsed")
    with c2: lon_val = st.text_input("Lon", value="49.889897", label_visibility="collapsed")
    
    if st.button("🎯 SYNC LOCATION"):
        st.session_state.lat = float(lat_val)
        st.session_state.lon = float(lon_val)
        st.rerun()

    st.markdown("<p style='font-size:11px; font-weight:700; color:#9ca3af; margin-top:10px;'>IMAGERY</p>", unsafe_allow_html=True)
    t0 = st.file_uploader("T0", type=["png","jpg"], label_visibility="collapsed")
    t1 = st.file_uploader("T1", type=["png","jpg"], label_visibility="collapsed")
    
    if st.button("🚀 EXECUTE AI"):
        if t0 and t1: st.session_state.run = True
        else: st.error("Upload images!")

# --- ƏSAS EKRAN ---
col_map, col_metrics = st.columns([3.9, 1.1])

with col_map:
    # Koordinatları state-dən götürürük
    cur_lat = st.session_state.get('lat', 40.461023)
    cur_lon = st.session_state.get('lon', 49.889897)
    
    # Xəritə (VALUE ERROR FIX: tiles=None və TileLayer birlikdə)
    m = folium.Map(location=[cur_lat, cur_lon], zoom_start=18, tiles=None)
    
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Satellite View"
    ).add_to(m)
    
    folium.Marker([cur_lat, cur_lon], icon=folium.Icon(color="red", icon="screenshot", prefix='fa')).add_to(m)
    
    # Xəritəni göstər
    folium_static(m, width=1200, height=650)
    
    # Şəkillər xəritənin altında
    if t0 or t1:
        st.markdown("<br>", unsafe_allow_html=True)
        img_c1, img_c2 = st.columns(2)
        with img_c1:
            if t0: st.image(t0, caption="2024 Reference", use_container_width=True)
        with img_c2:
            if t1: st.image(t1, caption="2025 Current", use_container_width=True)

with col_metrics:
    st.markdown("### 📊 Metrics")
    st.markdown(f"""
    <div class="metric-box">
        <p style='color:#9ca3af;font-size:10px;font-weight:700;margin:0'>NEW BUILDINGS</p>
        <p style='color:white;font-size:26px;font-weight:800;margin:0'>6</p>
    </div>
    <div class="metric-box">
        <p style='color:#9ca3af;font-size:10px;font-weight:700;margin:0'>ACCURACY</p>
        <p style='color:#10b981;font-size:26px;font-weight:800;margin:0'>92.4%</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get('run', False):
        report = generate_pdf(cur_lat, cur_lon)
        st.download_button("📄 DOWNLOAD REPORT", data=report, file_name="report.pdf", use_container_width=True)

    st.markdown("<div style='margin-top:50px; color:#4b5563; font-size:10px; text-align:center'>SATELLA AI v3.2</div>", unsafe_allow_html=True)
