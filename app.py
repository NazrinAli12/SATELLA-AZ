import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF

# 1. Ekranın kənarlarındakı boşluqları sıfırlamaq və geniş rejim
st.set_page_config(page_title="Google AI Studio", layout="wide", initial_sidebar_state="expanded")

# 2. AI STUDIO EXACT CSS (Sıxılmış və professional interfeys)
st.markdown("""
    <style>
    /* Ümumi tənzimləmələr */
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Google Sans', sans-serif;
        background-color: #0b0d0e !important;
        overflow: hidden; /* Ekranın sürüşməsinin qarşısını alır */
    }

    /* Sol Sidebar - AI Studio Tünd Rəngi */
    [data-testid="stSidebar"] {
        background-color: #111418 !important;
        border-right: 1px solid #2d333b !important;
        width: 260px !important;
    }

    /* Padding-lərin ləğvi (Ekranı tam doldurmaq üçün) */
    [data-testid="stHeader"], .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Sağ Panel (Metrics) */
    [data-testid="column"]:nth-child(2) {
        background-color: #111418 !important;
        border-left: 1px solid #2d333b !important;
        padding: 20px !important;
        height: 100vh;
    }

    /* Sol Panel üçün brendinq */
    .brand-box {
        padding: 15px 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .brand-icon {
        background: #1a73e8;
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
    }
    .brand-text { color: #e8eaed; font-size: 16px; font-weight: 500; }

    /* AI Studio Göy Oval Düyməsi */
    div.stButton > button {
        background-color: #1a73e8 !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important; /* Tam oval */
        padding: 4px 20px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        width: auto !important;
        margin: 10px 0 !important;
    }

    /* Sidebar Inputları */
    .stTextInput input {
        background-color: #1a1f24 !important;
        border: 1px solid #3c4043 !important;
        border-radius: 4px !important;
        color: #e8eaed !important;
        font-size: 13px !important;
    }

    /* Raster Data Qutuları (AI Studio Style) */
    .upload-area {
        border: 1px dashed #3c4043;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        margin: 10px 0;
        color: #9aa0a6;
        font-size: 12px;
    }

    /* Xəritə sahəsi (Ekrana sığması üçün) */
    .map-container {
        height: 100vh;
        width: 100%;
    }

    /* Metrik Kartları */
    .m-card {
        background: #1a1f24;
        border: 1px solid #3c4043;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .m-label { color: #9aa0a6; font-size: 10px; font-weight: 700; text-transform: uppercase; }
    .m-value { color: #e8eaed; font-size: 22px; font-weight: 500; }
    
    /* PDF Düyməsi (Google AI Studio Ağ Düymə) */
    .stDownloadButton button {
        background-color: #ffffff !important;
        color: #202124 !important;
        border-radius: 4px !important;
        border: none !important;
        font-weight: 500 !important;
        width: 100% !important;
        height: 36px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. PDF Generator (Stabil)
def generate_pdf_report(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"SATELLA Analysis Report - {datetime.now().date()}", ln=True)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 10, f"Coordinates: {lat}, {lon}", ln=True)
    return bytes(pdf.output())

# --- LAYOUT STRUKTURU ---
col_map, col_metrics = st.columns([4, 1.2], gap="small")

# --- SOL SIDEBAR (AI STUDIO CLONE) ---
with st.sidebar:
    st.markdown('<div class="brand-box"><div class="brand-icon">S</div><div class="brand-text">SATELLA</div></div>', unsafe_allow_html=True)
    
    st.markdown("<p style='color:#9aa0a6; font-size:11px; font-weight:700; margin-top:10px;'>AREA OF INTEREST</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: lat_val = st.text_input("Lat", "40.4093", label_visibility="collapsed")
    with c2: lon_val = st.text_input("Lon", "49.8671", label_visibility="collapsed")
    
    st.button("Zoom to Coordinate") # Oval göy düymə

    st.markdown("<p style='color:#9aa0a6; font-size:11px; font-weight:700; margin-top:20px;'>RASTER DATA</p>", unsafe_allow_html=True)
    
    st.markdown('<div class="upload-area">Baseline (T0).tif</div>', unsafe_allow_html=True)
    st.file_uploader("T0", label_visibility="collapsed", key="t0")
    
    st.markdown('<div class="upload-area">Current (T1).tif</div>', unsafe_allow_html=True)
    st.file_uploader("T1", label_visibility="collapsed", key="t1")
    
    st.markdown("<div style='margin-top:40px; color:#5f6368; font-size:10px;'>SATELLA v1.0<br>Sentinel-2 & Azercosmos</div>", unsafe_allow_html=True)

# --- MƏRKƏZ (XƏRİTƏ) ---
with col_map:
    # Ekrana tam sığması üçün hündürlük tənzimləndi
    current_lat = float(st.session_state.get('lat', 40.4093))
    current_lon = float(st.session_state.get('lon', 49.8671))
    
    m = folium.Map(location=[current_lat, current_lon], zoom_start=15, tiles="OpenStreetMap")
    folium.Marker([current_lat, current_lon]).add_to(m)
    folium_static(m, width=1250, height=880) # Hündürlük artırıldı, ekrana uyğunlaşdı

# --- SAĞ PANEL (METRICS & DOWNLOAD) ---
with col_metrics:
    st.markdown('<p style="color:#e8eaed; font-size:16px; font-weight:500; margin-bottom:20px;">System Metrics</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="m-card"><p class="m-label">NEW STRUCTURES</p><p class="m-value">6</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="m-card"><p class="m-label">PRECISION (IOU)</p><p class="m-value">92%</p></div>', unsafe_allow_html=True)
    
    # PDF Düyməsi
    report_data = generate_pdf_report(current_lat, current_lon)
    st.download_button(
        label="Generate PDF Report",
        data=report_data,
        file_name="satella_report.pdf",
        mime="application/pdf",
        use_container_width=True
    )
