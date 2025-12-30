import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io

# 1. Page Config
st.set_page_config(page_title="SATELLA | AI Studio", layout="wide", initial_sidebar_state="expanded")

# 2. UI FIXED CSS (Xəritənin itməməsi və Sağ Panelin düzgün görünməsi üçün)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Inter', sans-serif;
        background-color: #0b0d0e !important;
        overflow: hidden !important;
        margin: 0; padding: 0;
    }

    [data-testid="stHeader"] { display: none; }
    .block-container { padding: 0 !important; }

    /* SOL SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #111418 !important;
        border-right: 1px solid #2d333b !important;
        width: 250px !important;
    }

    /* SAĞ PANEL (FIXED) */
    .right-panel {
        position: fixed;
        right: 0; top: 0;
        width: 320px;
        height: 100vh;
        background-color: #111418;
        border-left: 1px solid #2d333b;
        padding: 24px;
        z-index: 1000;
        color: white;
    }

    /* XƏRİTƏ SAHƏSİ */
    .map-container {
        margin-right: 320px; /* Sağ panelə yer saxlayır */
        height: 100vh;
        width: calc(100% - 320px);
    }

    /* AI Studio Inputs & Buttons */
    .stTextInput input {
        background-color: #1a1f24 !important;
        border: 1px solid #3c4043 !important;
        border-radius: 6px !important;
        color: #e8eaed !important;
    }

    div.stButton > button {
        background-color: #1a73e8 !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        font-weight: 500 !important;
        width: 100% !important;
    }

    /* Metric Boxes */
    .m-card {
        background: #1a1f24;
        border: 1px solid #3c4043;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 12px;
    }
    .m-label { color: #9aa0a6; font-size: 10px; font-weight: 700; text-transform: uppercase; }
    .m-value { color: #ffffff; font-size: 20px; font-weight: 600; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

# 3. Session State for Coordinates
if 'lat' not in st.session_state:
    st.session_state.lat = 40.461023
if 'lon' not in st.session_state:
    st.session_state.lon = 49.889897

# --- SOL SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:white; font-size:18px;'>🛰️ SATELLA AI</h2>", unsafe_allow_html=True)
    
    st.markdown("<p style='color:#9aa0a6; font-size:11px; font-weight:700;'>TARGET COORDINATES</p>", unsafe_allow_html=True)
    new_lat = st.text_input("Latitude", str(st.session_state.lat), key="lat_input")
    new_lon = st.text_input("Longitude", str(st.session_state.lon), key="lon_input")
    
    if st.button("🔍 Analyze Location"):
        st.session_state.lat = float(new_lat)
        st.session_state.lon = float(new_lon)
        st.rerun()

    st.markdown("<br><p style='color:#9aa0a6; font-size:11px; font-weight:700;'>DATA SOURCE</p>", unsafe_allow_html=True)
    st.file_uploader("Upload Baseline", type=['png','jpg'], label_visibility="collapsed")
    st.file_uploader("Upload Current", type=['png','jpg'], label_visibility="collapsed")

# --- ANA EKRAN (MAP) ---
# Sağ paneli HTML ilə sabitləyirik ki, Streamlit sütunları xəritəni əzməsin
st.markdown(f"""
    <div class="right-panel">
        <p style='font-size:16px; font-weight:500; margin-bottom:20px;'>Detection Metrics</p>
        <div class="m-card">
            <div class="m-label">New Structures</div>
            <div class="m-value">6 detected</div>
        </div>
        <div class="m-card">
            <div class="m-label">Confidence Score</div>
            <div class="m-value">92.4%</div>
        </div>
        <div class="m-card">
            <div class="m-label">Coordinates</div>
            <div class="m-value" style="font-size:12px;">{st.session_state.lat}, {st.session_state.lon}</div>
        </div>
        <hr style="border:0.1px solid #2d333b; margin:20px 0;">
        <p style='color:#9aa0a6; font-size:11px;'>SYSTEM STATUS: <span style='color:#3fb950;'>● ACTIVE</span></p>
    </div>
""", unsafe_allow_html=True)

# Xəritə hissəsi
with st.container():
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    
    # Xəritəni yaradırıq
    m = folium.Map(
        location=[st.session_state.lat, st.session_state.lon], 
        zoom_start=18, 
        tiles="CartoDB dark_matter", 
        zoom_control=False
    )
    
    # Markeri əlavə et
    folium.Marker(
        [st.session_state.lat, st.session_state.lon],
        popup="Target Zone",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)
    
    # Radiusu göstər
    folium.Circle(
        [st.session_state.lat, st.session_state.lon],
        radius=100,
        color="#1a73e8",
        fill=True,
        fill_opacity=0.2
    ).add_to(m)

    folium_static(m, width=1200, height=900)
    st.markdown('</div>', unsafe_allow_html=True)
