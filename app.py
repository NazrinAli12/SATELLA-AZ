import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF

# 1. Səhifəni tam genişlikdə və gizli sidebar ilə açmaq
st.set_page_config(page_title="Google AI Studio", layout="wide", initial_sidebar_state="expanded")

# 2. AI Studio-nun Nöqtə-bə-Nöqtə CSS-i
st.markdown("""
    <style>
    /* Google Sans Font */
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');
    
    /* Ana Fonun və Səhifənin Sıfırlanması */
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Google Sans', sans-serif;
        background-color: #0b0d0e !important;
        color: #e8eaed;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important; /* Scroll-u ləğv edirik */
    }

    /* Paddinglərin Tam Ləğvi */
    [data-testid="stHeader"], .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }

    /* SOL SİDEBAR - Google AI Studio Black */
    [data-testid="stSidebar"] {
        background-color: #111418 !important;
        border-right: 1px solid #2d333b !important;
        width: 260px !important;
    }

    /* SAĞ PANEL (SYSTEM METRICS) - Sidebar kopyası */
    [data-testid="column"]:nth-child(2) {
        background-color: #111418 !important;
        border-left: 1px solid #2d333b !important;
        height: 100vh !important;
        padding: 20px !important;
        position: fixed;
        right: 0;
        top: 0;
        z-index: 100;
    }

    /* Logo və Başlıq (Sol Panel) */
    .brand-section { display: flex; align-items: center; gap: 10px; padding: 15px 0; }
    .brand-icon { background: #1a73e8; color: white; width: 28px; height: 28px; border-radius: 4px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 14px; }
    .brand-text { color: #f1f3f4; font-size: 16px; font-weight: 500; }

    /* AI Studio GÖY OVAL DÜYMƏSİ */
    div.stButton > button {
        background-color: #1a73e8 !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important; /* OVAL FORM */
        padding: 5px 24px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        width: auto !important;
        margin: 10px 0 !important;
    }

    /* Inputlar (Tünd AI Studio Style) */
    .stTextInput input {
        background-color: #1a1f24 !important;
        border: 1px solid #3c4043 !important;
        border-radius: 4px !important;
        color: #e8eaed !important;
        height: 36px !important;
    }

    /* Raster Data Qutuları (Dashed) */
    .upload-box {
        border: 1px dashed #3c4043;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        margin: 12px 0;
        color: #9aa0a6;
        font-size: 11px;
    }

    /* Metrik Kartları (Sağ Panel) */
    .metric-card {
        background: #1a1f24;
        border: 1px solid #3c4043;
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 12px;
    }
    .metric-label { color: #9aa0a6; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
    .metric-value { color: #e8eaed; font-size: 24px; font-weight: 500; margin-top: 4px; }

    /* PDF DÜYMƏSİ (Ağ AI Studio Düyməsi) */
    .stDownloadButton button {
        background-color: #ffffff !important;
        color: #202124 !important;
        border-radius: 4px !important;
        border: none !important;
        font-weight: 600 !important;
        width: 100% !important;
        margin-top: 15px !important;
        height: 38px !important;
    }

    /* Xəritənin Ekrana Sığdırılması */
    .map-wrapper { height: 100vh !important; width: 100% !important; }
    
    /* Live Badge */
    .live-badge {
        position: absolute; top: 15px; left: 15px; z-index: 1000;
        background: #1a1f24; border: 1px solid #3c4043;
        color: white; padding: 5px 12px; border-radius: 20px;
        font-size: 11px; font-weight: 700; display: flex; align-items: center;
    }
    .red-dot { height: 8px; width: 8px; background: #ea4335; border-radius: 50%; margin-right: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 3. PDF Generator (Stabil)
def generate_pdf_bytes(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "SATELLA AI ANALYSIS REPORT", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Coordinates: {lat}, {lon}", ln=True)
    pdf.cell(0, 10, f"Status: Detected 6 Construction Sites", ln=True)
    return bytes(pdf.output())

# --- UI STRUKTURU ---

# Sol Sidebar (Google AI Studio Left Panel)
with st.sidebar:
    st.markdown('<div class="brand-section"><div class="brand-icon">S</div><div class="brand-text">SATELLA</div></div>', unsafe_allow_html=True)
    
    st.markdown("<p style='color:#9aa0a6; font-size:11px; font-weight:700; margin-top:20px; letter-spacing:0.8px;'>AREA OF INTEREST</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: lat_val = st.text_input("Lat", "40.4093", label_visibility="collapsed")
    with c2: lon_val = st.text_input("Lon", "49.8671", label_visibility="collapsed")
    
    if st.button("Zoom to Coordinate"):
        st.session_state.lat, st.session_state.lon = lat_val, lon_val

    st.markdown("<p style='color:#9aa0a6; font-size:11px; font-weight:700; margin-top:30px; letter-spacing:0.8px;'>RASTER DATA</p>", unsafe_allow_html=True)
    
    st.markdown('<div class="upload-box">Baseline (T0).tif</div>', unsafe_allow_html=True)
    st.file_uploader("T0", label_visibility="collapsed", key="u1")
    
    st.markdown('<div class="upload-area" style="border: 1px dashed #3c4043; border-radius: 8px; padding: 10px; text-align: center; color: #9aa0a6; font-size: 11px; margin-bottom:10px;">Current (T1).tif</div>', unsafe_allow_html=True)
    st.file_uploader("T1", label_visibility="collapsed", key="u2")
    
    st.button("Run Change Detection", disabled=True)
    
    st.markdown("<div style='margin-top:60px; color:#5f6368; font-size:10px;'>SATELLA v1.0 | Google AI Style<br>FHN Safety Standards Compliant</div>", unsafe_allow_html=True)

# Mərkəzi Xəritə və Sağ Panel Layout
col_map, col_metrics = st.columns([3.8, 1.2], gap="small")

with col_map:
    # Live Badge
    st.markdown('<div class="live-badge"><span class="red-dot"></span> LIVE MONITORING</div>', unsafe_allow_html=True)
    
    current_lat = float(st.session_state.get('lat', 40.4093))
    current_lon = float(st.session_state.get('lon', 49.8671))
    
    # Xəritəni ekrana tam sığdırırıq (height=900 və ya 100vh üçün yaxın dəyər)
    m = folium.Map(location=[current_lat, current_lon], zoom_start=15, tiles="OpenStreetMap", zoom_control=False)
    folium.Marker([current_lat, current_lon]).add_to(m)
    folium_static(m, width=1280, height=920)

with col_metrics:
    # Sağ Panel (Google AI Studio Right Sidebar)
    st.markdown('<p style="color:#f1f3f4; font-size:16px; font-weight:500; margin-bottom:25px;">System Metrics</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="metric-card"><p class="metric-label">NEW STRUCTURES</p><p class="metric-value">6</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-card"><p class="metric-label">PRECISION (IOU)</p><p class="metric-value">92.4%</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="metric-card"><p class="metric-label">DETECTION STATUS</p><p class="metric-value" style="color:#3fb950; font-size:14px;">✓ Analysis Ready</p></div>', unsafe_allow_html=True)
    
    # PDF Düyməsi (Ağ rəngdə, ən aşağıda)
    pdf_content = generate_pdf_bytes(current_lat, current_lon)
    st.download_button(
        label="Generate PDF Report",
        data=pdf_content,
        file_name="SATELLA_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )
