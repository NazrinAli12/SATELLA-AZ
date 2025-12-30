import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF

# 1. Page Config
st.set_page_config(page_title="Google AI Studio", layout="wide", initial_sidebar_state="expanded")

# 2. AI STUDIO FULL UI CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    /* Ana Ekran Tənzimləmələri */
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Inter', sans-serif;
        background-color: #0b0d0e !important;
        margin: 0 !important; padding: 0 !important;
        overflow: hidden !important;
    }

    /* Boşluqların Ləğvi */
    [data-testid="stHeader"], .block-container {
        padding: 0 !important; margin: 0 !important;
    }

    /* SOL SİDEBAR - AI Studio Black */
    [data-testid="stSidebar"] {
        background-color: #111418 !important;
        border-right: 1px solid #2d333b !important;
        width: 280px !important;
    }

    /* SAĞ PANEL - Fixed Metrics Sidebar */
    [data-testid="column"]:nth-child(2) {
        background-color: #111418 !important;
        border-left: 1px solid #2d333b !important;
        height: 100vh !important;
        padding: 24px !important;
        position: fixed; right: 0; top: 0; z-index: 1000;
        overflow-y: auto;
    }

    /* Sol Panel Brending */
    .brand-container { display: flex; align-items: center; gap: 12px; padding: 20px 0; }
    .brand-icon { background: #1a73e8; color: white; width: 32px; height: 32px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-weight: bold; }
    .brand-text { font-size: 16px; font-weight: 500; color: #f1f3f4; letter-spacing: 0.5px; }

    /* AI Studio Göy Oval Düymə */
    div.stButton > button {
        background-color: #1a73e8 !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 6px 24px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        width: 100% !important;
        margin: 15px 0 !important;
    }

    /* Input Stili */
    .stTextInput input {
        background-color: #1a1f24 !important;
        border: 1px solid #3c4043 !important;
        border-radius: 6px !important;
        color: #e8eaed !important;
        font-size: 13px !important;
    }

    /* Raster Data Qutuları */
    .file-box {
        border: 1px dashed #3c4043;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        color: #9aa0a6;
        font-size: 11px;
        margin: 10px 0;
    }

    /* Sağ Panel Metrik Kartları */
    .m-card {
        background: #1a1f24;
        border: 1px solid #3c4043;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
    .m-label { color: #9aa0a6; font-size: 10px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px; }
    .m-value { color: #f1f3f4; font-size: 24px; font-weight: 500; }

    /* SAĞ PANEL PDF DÜYMƏSİ (Google White) */
    .stDownloadButton button {
        background-color: #ffffff !important;
        color: #111418 !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        height: 42px !important;
        width: 100% !important;
        margin-top: 20px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.2);
    }
    
    /* Live Indicator */
    .live-badge {
        position: absolute; top: 15px; left: 15px; z-index: 500;
        background: #1a1f24; border: 1px solid #3c4043;
        padding: 6px 14px; border-radius: 20px;
        color: white; font-size: 11px; font-weight: 600;
        display: flex; align-items: center;
    }
    .dot { height: 8px; width: 8px; background: #ea4335; border-radius: 50%; margin-right: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 3. PDF Function (Fixed Bytes)
def get_pdf_data(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 15, "SATELLA SYSTEM REPORT", ln=True, align='C')
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 10, f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(0, 10, f"Detection Coordinates: {lat}, {lon}", ln=True)
    pdf.cell(0, 10, "Result: 6 anomalies found.", ln=True)
    return bytes(pdf.output())

# --- UI STRUCTURE ---

# Sol Sidebar (1:1 AI Studio)
with st.sidebar:
    st.markdown('<div class="brand-container"><div class="brand-icon">S</div><div class="brand-text">SATELLA</div></div>', unsafe_allow_html=True)
    
    st.markdown("<p style='color:#9aa0a6; font-size:11px; font-weight:700; margin-top:10px;'>AREA OF INTEREST</p>", unsafe_allow_html=True)
    l1 = st.text_input("Lat", "40.4093", key="lat", label_visibility="collapsed")
    l2 = st.text_input("Lon", "49.8671", key="lon", label_visibility="collapsed")
    
    if st.button("Zoom to Coordinate"):
        st.session_state.clat, st.session_state.clon = l1, l2

    st.markdown("<p style='color:#9aa0a6; font-size:11px; font-weight:700; margin-top:25px;'>RASTER DATA</p>", unsafe_allow_html=True)
    st.markdown('<div class="file-box">Baseline (T0).tif</div>', unsafe_allow_html=True)
    st.file_uploader("a", label_visibility="collapsed", key="file_a")
    st.markdown('<div class="file-box">Current (T1).tif</div>', unsafe_allow_html=True)
    st.file_uploader("b", label_visibility="collapsed", key="file_b")

# Ana Layout (Xəritə və Sağ Sütun)
# Gap parametrini silərək xətanı ləğv etdik, CSS ilə tənzimlədik.
col_map, col_right = st.columns([4.2, 1.3])

with col_map:
    # Live Badge UI Studio stilində
    st.markdown('<div class="live-badge"><span class="dot"></span> LIVE MONITORING</div>', unsafe_allow_html=True)
    
    curr_lat = float(st.session_state.get('clat', 40.4093))
    curr_lon = float(st.session_state.get('clon', 49.8671))
    
    # Xəritə sahəsi (Ekrana tam sığan)
    m = folium.Map(location=[curr_lat, curr_lon], zoom_start=15, tiles="OpenStreetMap", zoom_control=False)
    folium_static(m, width=1350, height=950)

with col_right:
    # Sağ Sidebar Metriklər
    st.markdown('<p style="color:#f1f3f4; font-size:16px; font-weight:500; margin-bottom:20px;">System Metrics</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="m-card"><p class="m-label">NEW STRUCTURES</p><p class="m-value">6</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="m-card"><p class="m-label">PRECISION (IOU)</p><p class="m-value">92.4%</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="m-card"><p class="m-label">RECALL RATE</p><p class="m-value">88.1%</p></div>', unsafe_allow_html=True)
    
    # PDF Düyməsi (Xətasız və stabil)
    pdf_out = get_pdf_data(curr_lat, curr_lon)
    st.download_button(
        label="Generate PDF Report",
        data=pdf_out,
        file_name="satella_fhn_report.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    
    st.markdown("<div style='margin-top:40px; color:#5f6368; font-size:10px;'>SATELLA v1.2.0<br>AI Studio Professional Architecture</div>", unsafe_allow_html=True)
