import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF

# 1. Page Config - Tam ekran və tünd rejim
st.set_page_config(page_title="Google AI Studio", layout="wide", initial_sidebar_state="expanded")

# 2. AI STUDIO FULL UI MIRROR (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    /* Ana Ekranı Dondurmaq */
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Inter', sans-serif;
        background-color: #0b0d0e !important;
        color: #e8eaed;
        margin: 0 !important; padding: 0 !important;
        overflow: hidden !important; /* Ümumi scrollu ləğv edir */
    }

    /* Streamlit Padding ləğvi */
    [data-testid="stHeader"], .block-container {
        padding: 0 !important; margin: 0 !important;
    }

    /* SOL SİDEBAR - Tam AI Studio (Scrollsuz) */
    [data-testid="stSidebar"] {
        background-color: #111418 !important;
        border-right: 1px solid #2d333b !important;
        width: 250px !important;
        overflow: hidden !important; /* SOLDA SCROLL-U TAM LƏĞV EDİR */
    }
    
    /* Sidebar elementlərini sıxlaşdır */
    [data-testid="stSidebarUserContent"] {
        padding: 12px 16px !important;
    }

    /* SAĞ PANEL (Fixed Settings) */
    [data-testid="column"]:nth-child(2) {
        background-color: #111418 !important;
        border-left: 1px solid #2d333b !important;
        height: 100vh !important;
        padding: 20px !important;
        position: fixed; right: 0; top: 0;
        z-index: 1000;
    }

    /* AI Studio Brending */
    .brand-box { display: flex; align-items: center; gap: 10px; margin-bottom: 20px; }
    .brand-icon { background: #1a73e8; color: white; width: 28px; height: 28px; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px; }
    .brand-name { font-size: 15px; font-weight: 500; color: #f1f3f4; letter-spacing: 0.3px; }

    /* AI Studio GÖY OVAL DÜYMƏ */
    div.stButton > button {
        background-color: #1a73e8 !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important; /* Oval */
        padding: 4px 20px !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        width: 100% !important;
        margin: 8px 0 !important;
        transition: 0.2s;
    }
    div.stButton > button:hover { background-color: #1557b0 !important; }

    /* Input və File Uploader Sıxlığı */
    .stTextInput { margin-bottom: -20px !important; }
    .stFileUploader { margin-bottom: -15px !important; }
    
    .stTextInput input {
        background-color: #1a1f24 !important;
        border: 1px solid #3c4043 !important;
        border-radius: 6px !important;
        color: white !important;
        font-size: 12px !important;
        height: 32px !important;
    }

    /* Raster Data Box (Dashed AI Style) */
    .upload-container {
        border: 1px dashed #3c4043;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        color: #9aa0a6;
        font-size: 11px;
        margin: 5px 0;
        background: rgba(255,255,255,0.01);
    }

    /* Sağ Panel Metrik Kartları */
    .m-card {
        background: #1a1f24;
        border: 1px solid #3c4043;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .m-label { color: #9aa0a6; font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
    .m-value { color: #f1f3f4; font-size: 22px; font-weight: 500; }

    /* SAĞ PANEL PDF DÜYMƏSİ (Google White) */
    .stDownloadButton button {
        background-color: #ffffff !important;
        color: #111418 !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        height: 40px !important;
        width: 100% !important;
        margin-top: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. PDF Generator (Stabil)
def generate_pdf_bytes(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "SATELLA AI ANALYSIS REPORT", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Analysis Coordinate: {lat}, {lon}", ln=True)
    return bytes(pdf.output())

# --- SOL SIDEBAR (FIXED & NO SCROLL) ---
with st.sidebar:
    st.markdown('<div class="brand-box"><div class="brand-icon">S</div><div class="brand-name">SATELLA</div></div>', unsafe_allow_html=True)
    
    st.markdown("<p style='color:#9aa0a6; font-size:10px; font-weight:700; margin-bottom:5px;'>AREA OF INTEREST</p>", unsafe_allow_html=True)
    la = st.text_input("Lat", "40.4093", key="lat_in", label_visibility="collapsed")
    lo = st.text_input("Lon", "49.8671", key="lon_in", label_visibility="collapsed")
    
    if st.button("Zoom to Coordinate"):
        st.session_state.c_lat, st.session_state.c_lon = la, lo

    st.markdown("<p style='color:#9aa0a6; font-size:10px; font-weight:700; margin-top:15px;'>RASTER DATA</p>", unsafe_allow_html=True)
    
    st.markdown('<div class="upload-container">Baseline (T0).tif</div>', unsafe_allow_html=True)
    st.file_uploader("1", label_visibility="collapsed", key="file1")
    
    st.markdown('<div class="upload-container">Current (T1).tif</div>', unsafe_allow_html=True)
    st.file_uploader("2", label_visibility="collapsed", key="file2")
    
    st.markdown("<div style='position:absolute; bottom:20px; left:16px; color:#5f6368; font-size:9px;'>SATELLA v1.2.8 | AI Studio Layout</div>", unsafe_allow_html=True)

# --- ANA LAYOUT ---
# Sütunlar arası boşluq (gap) CSS ilə idarə olunur
col_map, col_right = st.columns([4.2, 1.2])

with col_map:
    clat = float(st.session_state.get('c_lat', 40.4093))
    clon = float(st.session_state.get('c_lon', 49.8671))
    
    # Xəritə sahəsi (Tam ekran hündürlüyü)
    m = folium.Map(location=[clat, clon], zoom_start=15, tiles="OpenStreetMap", zoom_control=False)
    folium.Marker([clat, clon]).add_to(m)
    folium_static(m, width=1350, height=1000)

with col_right:
    st.markdown('<p style="color:#f1f3f4; font-size:15px; font-weight:500; margin-bottom:15px;">System Metrics</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="m-card"><p class="m-label">NEW STRUCTURES</p><p class="m-value">6</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="m-card"><p class="m-label">PRECISION (IOU)</p><p class="m-value">92.4%</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="m-card"><p class="m-label">STATUS</p><p class="m-value" style="font-size:14px; color:#3fb950;">✓ Ready</p></div>', unsafe_allow_html=True)
    
    # PDF Düyməsi
    pdf_out = generate_pdf_bytes(clat, clon)
    st.download_button("Generate FHN Report", data=pdf_out, file_name="Report.pdf", use_container_width=True)
