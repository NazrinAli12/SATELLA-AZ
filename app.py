import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io
from PIL import Image

# 1. Səhifə Konfiqurasiyası
st.set_page_config(page_title="SATELLA AI", layout="wide", initial_sidebar_state="expanded")

# 2. UI Təkmilləşdirməsi (Professional Dark Palette)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Inter', sans-serif;
        background-color: #0b0d0e !important;
        overflow: hidden !important;
    }

    [data-testid="stHeader"] { display: none; }

    /* SOL SİDEBAR - Professional Style */
    section[data-testid="stSidebar"] {
        width: 320px !important;
        background-color: #0d1117 !important;
        border-right: 1px solid #30363d !important;
    }
    
    /* Loqo Hissəsi (Professional Card) */
    .brand-card {
        background: linear-gradient(145deg, #161b22, #0d1117);
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #30363d;
        margin-bottom: 1.5rem;
        text-align: left;
    }
    
    .brand-title {
        color: #f0f6fc;
        font-size: 18px;
        font-weight: 700;
        letter-spacing: 1px;
        margin: 0;
    }
    
    .brand-subtitle {
        color: #8b949e;
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 4px;
    }

    /* Düymələr (Professional Blue/Grey) */
    div.stButton > button {
        background: #238636 !important; /* Run düyməsi üçün yaşıl daha stabil görünür */
        border-radius: 6px !important;
        font-weight: 600 !important;
        height: 40px !important;
        width: 100%;
        border: 1px solid rgba(240,246,252,0.1) !important;
        font-size: 13px !important;
        color: white !important;
        margin-top: 15px;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background: #2ea043 !important;
        border-color: #f0f6fc !important;
    }

    /* Input Sahələri */
    .stTextInput input {
        background-color: #0d1117 !important;
        border: 1px solid #30363d !important;
        color: #c9d1d9 !important;
    }

    .sidebar-label {
        font-size: 10px;
        font-weight: 700;
        color: #8b949e;
        margin-bottom: 6px;
        margin-top: 15px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }

    .metric-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    
    /* PDF Düyməsi (Steel Blue) */
    .stDownloadButton button {
        background: #1f6feb !important;
        color: white !important;
        border-radius: 6px !important;
        height: 38px !important;
        width: 100%;
        font-size: 12px !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Funksiyalar (Eyni qalır)
def process_images(img1, img2):
    i1 = Image.open(img1)
    i2 = Image.open(img2)
    target_size = (1024, 768)
    return i1.resize(target_size, Image.Resampling.LANCZOS), i2.resize(target_size, Image.Resampling.LANCZOS)

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
    # Yenilənmiş Professional Loqo Hissəsi
    st.markdown("""
    <div class="brand-card">
        <p class="brand-title">🛰️ SATELLA</p>
        <p class="brand-subtitle">Enterprise AI Monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p class='sidebar-label'>Geospatial Focus</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        lat_val = st.text_input("LAT", value="40.394799", key="lat_in", label_visibility="collapsed")
    with c2:
        lon_val = st.text_input("LON", value="49.849585", key="lon_in", label_visibility="collapsed")
    
    st.markdown("<p class='sidebar-label'>Imagery Pipelines</p>", unsafe_allow_html=True)
    
    st.markdown("<p style='font-size:11px; color:#8b949e; margin-bottom:5px'>T0: Baseline Reference</p>", unsafe_allow_html=True)
    t0_file = st.file_uploader("u1", type=["png","jpg"], label_visibility="collapsed", key="u1")
    
    st.markdown("<p style='font-size:11px; color:#8b949e; margin-bottom:5px; margin-top:10px'>T1: Analysis Target</p>", unsafe_allow_html=True)
    t1_file = st.file_uploader("u2", type=["png","jpg"], label_visibility="collapsed", key="u2")
    
    if st.button("EXECUTE ANALYSIS"):
        if t0_file and t1_file:
            st.session_state.lat = float(lat_val)
            st.session_state.lon = float(lon_val)
            st.session_state.run = True
        else:
            st.error("Assets missing!")

# --- ƏSAS EKRAN ---
col_map, col_metrics = st.columns([3.9, 1.1])

with col_map:
    cur_lat = st.session_state.get('lat', 40.394799)
    cur_lon = st.session_state.get('lon', 49.849585)
    
    m = folium.Map(location=[cur_lat, cur_lon], zoom_start=17, tiles=None)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri", name="Satellite View"
    ).add_to(m)
    folium.Marker([cur_lat, cur_lon]).add_to(m)
    
    folium_static(m, width=1200, height=600)
    
    if t0_file and t1_file:
        img1, img2 = process_images(t0_file, t1_file)
        st.markdown("<br>", unsafe_allow_html=True)
        img_c1, img_c2 = st.columns(2)
        with img_c1:
            st.image(img1, caption="2024 Reference", use_container_width=True)
        with img_c2:
            st.image(img2, caption="2025 Current", use_container_width=True)

with col_metrics:
    st.markdown("<p style='font-weight:700; color:#f0f6fc; font-size:14px; margin-bottom:20px'>DATA INSIGHTS</p>", unsafe_allow_html=True)
    
    metrics = [
        ("DETECTION COUNT", "1", "#f0f6fc"),
        ("PRECISION RATE", "92%", "#58a6ff"),
        ("F1 PERFORMANCE", "90%", "#3fb950")
    ]
    
    for label, val, color in metrics:
        st.markdown(f"""
        <div class="metric-box">
            <p style='color:#8b949e; font-size:9px; font-weight:700; margin:0'>{label}</p>
            <p style='color:{color}; font-size:24px; font-weight:800; margin:0'>{val}</p>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.get('run', False):
        report = generate_pdf(cur_lat, cur_lon)
        st.download_button("📥 GENERATE PDF REPORT", data=report, file_name="satella_report.pdf", use_container_width=True)

    st.markdown("<div style='margin-top:40px; color:#484f58; font-size:9px; text-align:center; font-weight:600'>SATELLA SYSTEMS v3.2</div>", unsafe_allow_html=True)
