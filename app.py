import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io

# 1. Səhifə konfiqurasiyası
st.set_page_config(page_title="SATELLA | AI Studio", layout="wide", initial_sidebar_state="expanded")

# 2. UI TƏKMİLLƏŞDİRMƏ (Xəritə ölçüsü və Sağ Panel daxil)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    /* Ana Ekran Arxivlənmiş Scroll-suz */
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Inter', sans-serif;
        background-color: #0b0d0e !important;
        overflow: hidden !important;
    }

    /* Streamlit-in standart artıq boşluqlarını silirik */
    [data-testid="stHeader"] { display: none; }
    .block-container { padding: 0 !important; max-width: 100% !important; }

    /* SOL SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #111418 !important;
        border-right: 1px solid #2d333b !important;
        width: 260px !important;
    }

    /* SAĞ PANEL - FIXED & DATA VISIBLE */
    [data-testid="column"]:nth-child(2) {
        background-color: #111418 !important;
        border-left: 1px solid #2d333b !important;
        position: fixed !important;
        right: 0;
        top: 0;
        width: 320px !important; /* Panel genişliyi sabitləndi */
        height: 100vh !important;
        padding: 25px 20px !important;
        z-index: 1000;
        overflow-y: auto;
        display: block !important;
    }

    /* XƏRİTƏ SAHƏSİ - Ölçü tənzimləməsi */
    [data-testid="column"]:nth-child(1) {
        width: calc(100% - 320px) !important; /* Xəritə sağ panelə yer saxlayır */
        padding-right: 20px;
    }

    /* Google AI Studio Düymə Stili */
    div.stButton > button {
        background-color: #1a73e8 !important;
        color: white !important;
        border-radius: 20px !important;
        border: none !important;
        font-size: 13px !important;
        height: 36px !important;
        transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #1557b0 !important; box-shadow: 0 0 10px rgba(26,115,232,0.4); }

    /* Metrika Kartları */
    .metric-card {
        background: #1a1f24;
        border: 1px solid #3c4043;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 12px;
    }
    .m-title { color: #9aa0a6; font-size: 10px; font-weight: 700; text-transform: uppercase; }
    .m-value { color: #ffffff; font-size: 22px; font-weight: 600; margin-top: 5px; }

    /* Progress Barlar */
    .p-bar-label { display: flex; justify-content: space-between; font-size: 11px; color: #9aa0a6; margin-bottom: 4px; }
    .p-bar-bg { background: #3c4043; height: 5px; border-radius: 3px; margin-bottom: 15px; }
    .p-bar-fill { height: 100%; border-radius: 3px; }

</style>
""", unsafe_allow_html=True)

# PDF Funksiyası
def get_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "SATELLA ANALYSIS REPORT", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- SOL SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:white; font-size:20px; margin-bottom:20px;'>🛰️ SATELLA</h2>", unsafe_allow_html=True)
    
    st.markdown("**Location Control**")
    lat_val = st.text_input("Latitude", "40.4093", label_visibility="collapsed")
    lon_val = st.text_input("Longitude", "49.8671", label_visibility="collapsed")
    
    if st.button("Update View", use_container_width=True):
        st.session_state.lat = float(lat_val)
        st.session_state.lon = float(lon_val)

    st.markdown("<br>**Satellite Feed**", unsafe_allow_html=True)
    st.file_uploader("T0 Baseline", type=['png','jpg','tif'], label_visibility="collapsed")
    st.file_uploader("T1 Current", type=['png','jpg','tif'], label_visibility="collapsed")

# --- ANA LAYOUT ---
c_map, c_data = st.columns([4, 1]) # Vizual olaraq bölünür, amma CSS bunu override edir

with c_map:
    # Live Badge
    st.markdown("<div style='position:absolute; top:20px; left:20px; z-index:999; background:rgba(17,20,24,0.8); padding:5px 15px; border-radius:20px; color:#3fb950; font-size:12px; border:1px solid #3c4043;'>● LIVE SYSTEM</div>", unsafe_allow_html=True)
    
    curr_lat = st.session_state.get('lat', 40.4093)
    curr_lon = st.session_state.get('lon', 49.8671)
    
    m = folium.Map([curr_lat, curr_lon], zoom_start=16, tiles="CartoDB dark_matter", zoom_control=False)
    folium.Circle([curr_lat, curr_lon], 300, color="#1a73e8", fill=True, opacity=0.2).add_to(m)
    folium_static(m, width=1150, height=880) # Xəritə genişliyi idarə altına alındı

with c_data:
    st.markdown("<p style='color:white; font-size:18px; font-weight:500;'>Analysis Results</p>", unsafe_allow_html=True)
    
    # Metrikalar
    st.markdown("""
        <div class="metric-card"><div class="m-title">New Structures</div><div class="m-value">6 detected</div></div>
        <div class="metric-card"><div class="m-title">Analyzed Area</div><div class="m-value">1.4 km²</div></div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Proqress Barlar
    stats = [("Precision", "92%", "#4285f4"), ("Recall", "88%", "#34a853"), ("F1-Score", "90%", "#a142f4")]
    for n, p, c in stats:
        st.markdown(f"""
            <div class="p-bar-label"><span>{n}</span><span>{p}</span></div>
            <div class="p-bar-bg"><div class="p-bar-fill" style="width:{p}; background:{c};"></div></div>
        """, unsafe_allow_html=True)

    if st.button("Generate Official Report", use_container_width=True):
        pdf_bytes = get_pdf(curr_lat, curr_lon)
        st.download_button("Download PDF", pdf_bytes, "Satella_Report.pdf", use_container_width=True)
    
    st.markdown("<div style='margin-top:30px; border:1px solid #ffab0033; background:#ffab0011; padding:10px; border-radius:8px; color:#ffab00; font-size:11px;'><b>Note:</b> Manual field verification is required for anomalies in zone A-4.</div>", unsafe_allow_html=True)
