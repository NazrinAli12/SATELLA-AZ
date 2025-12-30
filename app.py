import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io

# 1. Page Config
st.set_page_config(page_title="SATELLA", layout="wide", initial_sidebar_state="expanded")

# 2. UI Styling (Ultra Compact Sidebar + Fixed Layout)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Inter', sans-serif;
        background-color: #0b0d0e !important;
        overflow: hidden !important;
    }

    /* SOL SİDEBAR - Scroll yoxdur, hər şey sığır */
    section[data-testid="stSidebar"] {
        width: 360px !important;
        background-color: #111418 !important;
        border-right: 1px solid #2d333b !important;
    }
    section[data-testid="stSidebar"] > div {
        height: 100vh !important;
        overflow: hidden !important;
        padding: 1rem !important;
    }

    /* SAĞ PANEL */
    [data-testid="column"]:nth-child(2) {
        background-color: #111418 !important;
        border-left: 1px solid #2d333b !important;
        padding: 20px !important;
        height: 100vh;
    }

    /* Boşluqları sıxmaq */
    .stVerticalBlock { gap: 0.4rem !important; }
    div[data-testid="stFileUploader"] { margin-top: -10px; }

    /* Düymə və Metrika Kartları */
    div.stButton > button {
        background: #1a73e8 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        height: 38px !important;
    }
    .metric-card {
        background: #1a1f24;
        border: 1px solid #3c4043;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 8px;
    }
    
    /* Xəritənin ətrafında təmiz boşluq */
    .map-frame { border-radius: 12px; overflow: hidden; border: 1px solid #2d333b; }
</style>
""", unsafe_allow_html=True)

# 3. PDF Generator
def generate_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "SATELLA - Construction Report", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Location: {lat}, {lon}", ln=True)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- SOL SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1e3a8a,#3b82f6);padding:0.8rem;border-radius:10px;margin-bottom:1rem'>
        <h2 style='color:white;margin:0;font-size:18px;'>🛰️ SATELLA AI</h2>
        <p style='color:#bfdbfe;margin:0;font-size:10px'>Azerbaijan Monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-size:11px; font-weight:700; color:#9ca3af; margin-bottom:2px'>COORDINATES</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: lat_val = st.text_input("Lat", value="40.461023", label_visibility="collapsed")
    with c2: lon_val = st.text_input("Lon", value="49.889897", label_visibility="collapsed")
    
    if st.button("🎯 UPDATE MAP", use_container_width=True):
        st.session_state.current_lat = float(lat_val)
        st.session_state.current_lon = float(lon_val)
        st.rerun()
    
    st.markdown("<p style='font-size:11px; font-weight:700; color:#9ca3af; margin-top:10px; margin-bottom:2px'>RASTER FEED</p>", unsafe_allow_html=True)
    baseline = st.file_uploader("T0", type=["png","jpg"], key="t0", label_visibility="collapsed")
    current = st.file_uploader("T1", type=["png","jpg"], key="t1", label_visibility="collapsed")
    
    if st.button("🚀 EXECUTE AI", use_container_width=True):
        if baseline and current: 
            st.session_state.detection_run = True
        else: 
            st.error("Upload T0 & T1")

# --- ANA EKRAN ---
col_map, col_right = st.columns([3.9, 1.1])

with col_map:
    clat = st.session_state.get('current_lat', 40.461023)
    clon = st.session_state.get('current_lon', 49.889897)
    
    # Xəritə Obyekti (ValueError Fix: attr əlavə olundu)
    m = folium.Map(
        location=[clat, clon],
        zoom_start=18,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        zoom_control=False
    )
    folium.Marker([clat, clon], icon=folium.Icon(color="red", icon="crosshairs", prefix="fa")).add_to(m)
    
    st.markdown('<div class="map-frame">', unsafe_allow_html=True)
    folium_static(m, width=1180, height=620)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Şəkillər xəritənin altında səliqəli
    if baseline or current:
        st.markdown("<div style='margin-top:15px'></div>", unsafe_allow_html=True)
        img_c1, img_c2 = st.columns(2)
        with img_c1:
            if baseline: st.image(baseline, caption="2024 Reference", use_container_width=True)
        with img_c2:
            if current: st.image(current, caption="2025 Current", use_container_width=True)

with col_right:
    st.markdown("### 📊 Metrics")
    st.markdown(f"""
    <div class="metric-card">
        <p style='color:#9ca3af;font-size:10px;font-weight:700;margin:0'>STRUCTURES</p>
        <p style='color:white;font-size:26px;font-weight:800;margin:0'>6</p>
    </div>
    <div class="metric-card">
        <p style='color:#9ca3af;font-size:10px;font-weight:700;margin:0'>PRECISION</p>
        <p style='color:#10b981;font-size:26px;font-weight:800;margin:0'>92.4%</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get('detection_run', False):
        report_pdf = generate_pdf(clat, clon)
        st.download_button("📄 DOWNLOAD PDF", data=report_pdf, file_name="satella_report.pdf", use_container_width=True)
    
    st.markdown("<br><p style='color:#4b5563; font-size:10px; text-align:center'>v3.1.2 Production</p>", unsafe_allow_html=True)
