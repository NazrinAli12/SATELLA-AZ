import streamlit as st
import folium
from streamlit_folium import folium_static
from fpdf import FPDF
import io

# 1. Page Config
st.set_page_config(page_title="SATELLA | AI Studio", layout="wide", initial_sidebar_state="expanded")

# 2. Perfect UI CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Inter', sans-serif;
        background-color: #0b0d0e !important;
        overflow: hidden !important;
    }

    [data-testid="stHeader"] { display: none; }
    .block-container { padding: 0 !important; }

    /* SOL SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #111418 !important;
        border-right: 1px solid #2d333b !important;
        width: 260px !important;
    }

    /* SAĞ PANEL (FIXED & NON-BLOCKING) */
    .right-info-panel {
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

    /* XƏRİTƏNİN SAĞ PANELƏ GİRMƏMƏSİ ÜÇÜN KONTEYNER */
    .map-area {
        margin-right: 320px;
        height: 100vh;
    }

    /* AI STUDIO DÜYMƏLƏRİ */
    div.stButton > button {
        background-color: #1a73e8 !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        font-weight: 500 !important;
        height: 38px !important;
        width: 100% !important;
    }

    /* Inputlar */
    .stTextInput input {
        background-color: #1a1f24 !important;
        border: 1px solid #3c4043 !important;
        color: white !important;
        border-radius: 6px !important;
    }

    /* Metrika Kartları */
    .m-card {
        background: #1a1f24;
        border: 1px solid #3c4043;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Session State (Koordinatların dərhal yenilənməsi üçün)
if 'lat' not in st.session_state:
    st.session_state.lat = 40.461023
if 'lon' not in st.session_state:
    st.session_state.lon = 49.889897

# --- SOL SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:white; font-size:22px; margin-bottom:20px;'>🛰️ SATELLA</h2>", unsafe_allow_html=True)
    
    st.markdown("<p style='color:#9aa0a6; font-size:11px; font-weight:700;'>TARGET ZONE</p>", unsafe_allow_html=True)
    # On_change istifadə edərək birbaşa session yeniləyirik
    lat_input = st.text_input("Lat", value=str(st.session_state.lat))
    lon_input = st.text_input("Lon", value=str(st.session_state.lon))
    
    if st.button("RUN ANALYSIS / ZOOM"):
        st.session_state.lat = float(lat_input)
        st.session_state.lon = float(lon_input)
        st.rerun()

    st.markdown("<br><p style='color:#9aa0a6; font-size:11px; font-weight:700;'>IMAGERY</p>", unsafe_allow_html=True)
    st.file_uploader("Upload", label_visibility="collapsed")

# --- SAĞ PANEL (HTML/CSS ilə Sabitlənmiş) ---
st.markdown(f"""
    <div class="right-info-panel">
        <p style='font-size:18px; font-weight:500; margin-bottom:25px;'>Analysis Metrics</p>
        <div class="m-card">
            <p style='color:#9aa0a6; font-size:10px; margin:0;'>STRUCTURES FOUND</p>
            <p style='font-size:24px; font-weight:bold; margin:5px 0;'>6</p>
        </div>
        <div class="m-card">
            <p style='color:#9aa0a6; font-size:10px; margin:0;'>PRECISION</p>
            <p style='font-size:24px; font-weight:bold; margin:5px 0; color:#3fb950;'>92.4%</p>
        </div>
        <div class="m-card">
            <p style='color:#9aa0a6; font-size:10px; margin:0;'>COORDINATES</p>
            <p style='font-size:12px; margin:5px 0;'>{st.session_state.lat}, {st.session_state.lon}</p>
        </div>
        <p style='color:#5f6368; font-size:10px; margin-top:100px;'>v1.0.2 | Enterprise Ready</p>
    </div>
""", unsafe_allow_html=True)

# --- MƏRKƏZ (XƏRİTƏ) ---
# Xəritəni column daxilində deyil, birbaşa geniş sahədə yaradırıq
st.markdown('<div class="map-area">', unsafe_allow_html=True)

# Xəritə obyekti hər dəfə session_state ilə sıfırdan yaradılır (Bu, yeri işarələməni təmin edir)
m = folium.Map(
    location=[st.session_state.lat, st.session_state.lon],
    zoom_start=18,
    tiles="CartoDB dark_matter",
    zoom_control=False
)

# Qırmızı Marker (Tam mərkəz nöqtə)
folium.Marker(
    [st.session_state.lat, st.session_state.lon],
    icon=folium.Icon(color='red', icon='screenshot', prefix='fa')
).add_to(m)

# Təsir dairəsi (Mavi aura)
folium.Circle(
    [st.session_state.lat, st.session_state.lon],
    radius=100,
    color="#1a73e8",
    fill=True,
    fill_opacity=0.2
).add_to(m)

# Xəritəni Render et (Genişlik sağ paneli nəzərə alaraq tənzimlənir)
folium_static(m, width=1150, height=950)

st.markdown('</div>', unsafe_allow_html=True)
