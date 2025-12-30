import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF

# 1. Səhifəni tam doldurmaq üçün konfiqurasiya
st.set_page_config(page_title="Google AI Studio", layout="wide", initial_sidebar_state="expanded")

# 2. Xətaları aradan qaldıran və Vizualı kopyalayan CSS
st.markdown("""
    <style>
    /* Google Sans Stilini tətbiq et */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Inter', sans-serif;
        background-color: #0b0d0e !important;
        color: #e8eaed;
        margin: 0 !important; padding: 0 !important;
        overflow: hidden !important;
    }

    /* Streamlit-in standart boşluqlarını (Padding) məhv et */
    [data-testid="stHeader"], .block-container {
        padding: 0 !important; margin: 0 !important;
        max-width: 100% !important;
    }

    /* SOL PANEL - Google AI Studio Black */
    [data-testid="stSidebar"] {
        background-color: #111418 !important;
        border-right: 1px solid #2d333b !important;
        width: 260px !important;
    }

    /* SAĞ PANEL (Metrics) */
    [data-testid="column"]:nth-child(2) {
        background-color: #111418 !important;
        border-left: 1px solid #2d333b !important;
        height: 100vh !important;
        padding: 24px !important;
        position: fixed; right: 0; top: 0;
    }

    /* Logo və Başlıq */
    .brand { display: flex; align-items: center; gap: 10px; padding-bottom: 20px; }
    .b-icon { background: #1a73e8; color: white; width: 30px; height: 30px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-weight: bold; }
    .b-text { font-size: 16px; font-weight: 500; color: #f1f3f4; }

    /* AI STUDIO GÖY OVAL DÜYMƏ */
    div.stButton > button {
        background-color: #1a73e8 !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 6px 20px !important;
        font-size: 13px !important;
        width: 100% !important;
    }

    /* Input və Upload qutuları */
    .stTextInput input { background-color: #1a1f24 !important; border: 1px solid #3c4043 !important; color: white !important; }
    .up-box { border: 1px dashed #3c4043; border-radius: 8px; padding: 12px; text-align: center; color: #9aa0a6; font-size: 11px; margin: 10px 0; }

    /* Metrik Kartları (Sağ) */
    .m-card { background: #1a1f24; border: 1px solid #3c4043; border-radius: 8px; padding: 15px; margin-bottom: 12px; }
    .m-label { color: #9aa0a6; font-size: 10px; font-weight: 700; text-transform: uppercase; }
    .m-value { color: #e8eaed; font-size: 24px; font-weight: 500; }

    /* PDF DÜYMƏSİ (Google White Style) */
    .stDownloadButton button {
        background-color: #ffffff !important;
        color: #111418 !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        height: 40px !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. PDF Generator (Stabil Bayt formatı)
def make_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "SATELLA ANALYSIS REPORT", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 10, f"Location: {lat}, {lon}", ln=True)
    return bytes(pdf.output())

# --- SOL SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="brand"><div class="b-icon">S</div><div class="b-text">SATELLA</div></div>', unsafe_allow_html=True)
    
    st.markdown("<p style='color:#9aa0a6; font-size:11px; font-weight:700;'>AREA OF INTEREST</p>", unsafe_allow_html=True)
    lat_in = st.text_input("Lat", "40.4093", label_visibility="collapsed")
    lon_in = st.text_input("Lon", "49.8671", label_visibility="collapsed")
    
    if st.button("Zoom to Coordinate"):
        st.session_state.lat, st.session_state.lon = lat_in, lon_in

    st.markdown("<p style='color:#9aa0a6; font-size:11px; font-weight:700; margin-top:20px;'>RASTER DATA</p>", unsafe_allow_html=True)
    st.markdown('<div class="up-box">Baseline (T0).tif</div>', unsafe_allow_html=True)
    st.file_uploader("T0", label_visibility="collapsed", key="a")
    st.markdown('<div class="up-box">Current (T1).tif</div>', unsafe_allow_html=True)
    st.file_uploader("T1", label_visibility="collapsed", key="b")

# --- MƏRKƏZ VƏ SAĞ PANEL ---
# Column Gap xətası burada həll olundu (gap yoxdur, CSS ilə tənzimlənir)
c_map, c_met = st.columns([4, 1.3])

with c_map:
    # Xəritəni ekrana tam sığdırmaq üçün hündürlük 900+ seçildi
    clat = float(st.session_state.get('lat', 40.4093))
    clon = float(st.session_state.get('lon', 49.8671))
    
    m = folium.Map(location=[clat, clon], zoom_start=15, tiles="OpenStreetMap", zoom_control=False)
    folium_static(m, width=1300, height=950)

with c_met:
    st.markdown('<p style="color:#f1f3f4; font-size:16px; font-weight:500; margin-bottom:20px;">System Metrics</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="m-card"><p class="m-label">NEW STRUCTURES</p><p class="m-value">6</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="m-card"><p class="m-label">PRECISION (IOU)</p><p class="m-value">92.4%</p></div>', unsafe_allow_html=True)
    
    # PDF Düyməsi
    pdf_b = make_pdf(clat, clon)
    st.download_button("Generate PDF Report", data=pdf_b, file_name="report.pdf", use_container_width=True)

    st.markdown("<div style='margin-top:50px; color:#5f6368; font-size:10px;'>v1.0.2 | AI Studio UI</div>", unsafe_allow_html=True)
