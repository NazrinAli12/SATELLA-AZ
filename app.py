import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
from PIL import Image

# 1. SƏHİFƏ AYARLARI
st.set_page_config(
    page_title="SATELLA AI", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. RADİKAL CSS (Sidebar-ın itməsini fiziki olaraq bloklayır)
st.markdown("""
<style>
    /* Ana fon */
    .stApp { background-color: #0b0d0e; }

    /* SIDEBAR-I MƏCBURİ SABİTLƏMƏK */
    [data-testid="stSidebar"] {
        background-color: #0d1117 !important;
        min-width: 320px !important;
        max-width: 320px !important;
        border-right: 1px solid #30363d !important;
        visibility: visible !important;
        display: block !important;
    }

    /* Sidebar daxilindəki elementləri ağ rəng etmək */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Xəritənin kənarlara sıxılmaması üçün əsas konteynerə boşluq veririk */
    [data-testid="stHorizontalBlock"] {
        padding-left: 20px;
        padding-right: 20px;
    }

    /* Headeri gizlət */
    [data-testid="stHeader"] { display: none !important; }

    /* Brend Başlığı */
    .brand-box {
        background: #1f6feb;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 3. PDF FUNKSİYASI
def create_report(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, "SATELLA AI - MONITORING REPORT", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Location: {lat}, {lon}", ln=True)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- 🛰️ SOL PANEL (SIDEBAR) ---
with st.sidebar:
    st.markdown('<div class="brand-box"><h2 style="margin:0;color:white;">🛰️ SATELLA</h2></div>', unsafe_allow_html=True)
    
    st.markdown("### 📍 Location")
    lat_val = st.text_input("Latitude", value="40.394799", key="lat_field")
    lon_val = st.text_input("Longitude", value="49.849585", key="lon_field")
    
    if st.button("🎯 UPDATE VIEW", use_container_width=True):
        st.session_state.lat = float(lat_val)
        st.session_state.lon = float(lon_val)

    st.markdown("---")
    st.markdown("### 🛰️ Imagery")
    t0 = st.file_uploader("T0: 2024", type=["png", "jpg"], key="t0_up")
    t1 = st.file_uploader("T1: 2025", type=["png", "jpg"], key="t1_up")
    
    if st.button("🚀 EXECUTE AI", use_container_width=True):
        if t0 and t1:
            st.session_state.ready = True
            st.balloons()

# --- 🗺️ ƏSAS EKRAN ---
# Xəritəni sidebar-ı sıxışdırmasın deyə mütənasib ölçüdə saxlayırıq
col_main, col_stats = st.columns([3.5, 1])

with col_main:
    lat = st.session_state.get('lat', 40.394799)
    lon = st.session_state.get('lon', 49.849585)
    
    # Xəritə (ArcGIS Attribution düzəlişi ilə)
    m = folium.Map(location=[lat, lon], zoom_start=18)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri Satellite",
        name="Satellite"
    ).add_to(m)
    folium.Marker([lat, lon]).add_to(m)
    
    # Xəritə ölçüsü: Enini (width) çox böyük etmirik ki, sidebarı itirməsin
    folium_static(m, width=950, height=500)
    
    if t0 and t1:
        st.markdown("### 🔍 Image Sync")
        c1, c2 = st.columns(2)
        c1.image(t0, caption="2024 (T0)", use_container_width=True)
        c2.image(t1, caption="2025 (T1)", use_container_width=True)

with col_stats:
    st.markdown("### 📊 Metrics")
    detect = "1" if st.session_state.get('ready', False) else "0"
    
    st.markdown(f"""
    <div style="background:#161b22; padding:15px; border-radius:8px; border:1px solid #30363d; margin-bottom:10px;">
        <p style="color:#8b949e; font-size:12px; margin:0;">NEW BUILDINGS</p>
        <p style="color:white; font-size:24px; font-weight:bold; margin:0;">{detect}</p>
    </div>
    <div style="background:#161b22; padding:15px; border-radius:8px; border:1px solid #30363d;">
        <p style="color:#8b949e; font-size:12px; margin:0;">AI CONFIDENCE</p>
        <p style="color:#58a6ff; font-size:24px; font-weight:bold; margin:0;">92.4%</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get('ready', False):
        report = create_report(lat, lon)
        st.download_button("📥 DOWNLOAD REPORT", report, "report.pdf", use_container_width=True)

st.markdown("<hr><center style='color:grey; font-size:10px;'>SATELLA AI v3.3</center>", unsafe_allow_html=True)
