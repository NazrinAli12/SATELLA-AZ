import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io

# 1. Page Config
st.set_page_config(page_title="SATELLA | AI Studio", layout="wide", initial_sidebar_state="expanded")

# 2. UI MIRROR CSS (Şəkillərdəki tam görüntü)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    /* Ana fon və Scroll-un ləğvi */
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Inter', sans-serif;
        background-color: #0b0d0e !important;
        overflow: hidden !important;
    }

    [data-testid="stHeader"] { display: none; }
    .block-container { padding: 0 !important; }

    /* SOL SIDEBAR - Compact Style */
    section[data-testid="stSidebar"] {
        background-color: #111418 !important;
        border-right: 1px solid #2d333b !important;
        width: 260px !important;
    }
    section[data-testid="stSidebar"] > div { overflow: hidden !important; }
    
    /* SAĞ PANEL - Fixed Settings Panel (Şəkildəki kimi) */
    [data-testid="column"]:nth-child(2) {
        background-color: #111418 !important;
        border-left: 1px solid #2d333b !important;
        height: 100vh !important;
        padding: 20px 15px !important;
        position: fixed;
        right: 0; top: 0;
        z-index: 1000;
        overflow-y: auto;
    }

    /* AI Studio Inputlar */
    .stTextInput input {
        background-color: #1a1f24 !important;
        border: 1px solid #3c4043 !important;
        border-radius: 4px !important;
        color: #e8eaed !important;
    }

    /* Mavi "Zoom" və "Run" düymələri */
    div.stButton > button {
        background-color: #1a73e8 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        height: 38px !important;
        width: 100% !important;
    }

    /* Metrika Kartları (Şəkildəki Box-lar) */
    .metric-box {
        background: #1a1f24;
        border: 1px solid #3c4043;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    .metric-label { color: #9aa0a6; font-size: 10px; font-weight: 700; text-transform: uppercase; }
    .metric-value { color: #ffffff; font-size: 20px; font-weight: 600; margin-top: 4px; }

    /* Progress Barlar (Precision/Recall üçün) */
    .progress-wrapper { margin-bottom: 15px; }
    .progress-text { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px; color: #9aa0a6; }
    .bar-bg { background: #3c4043; height: 4px; border-radius: 2px; }
    .bar-fill { height: 4px; border-radius: 2px; }

    /* Warning Box */
    .warning-card {
        background: rgba(255, 171, 0, 0.05);
        border: 1px solid rgba(255, 171, 0, 0.2);
        padding: 12px;
        border-radius: 8px;
        color: #ffab00;
        font-size: 11px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# 3. PDF Generator
def generate_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "SATELLA - Construction Report", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Coordinate: {lat}, {lon}", ln=True)
    pdf.cell(0, 10, f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- SOL SIDEBAR ---
with st.sidebar:
    st.markdown("""
        <div style='display:flex; align-items:center; gap:10px; margin-bottom:20px'>
            <div style='background:#1a73e8; padding:5px 8px; border-radius:4px; font-weight:bold; color:white'>S</div>
            <div style='color:white; font-weight:600; font-size:16px'>SATELLA</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<p style='color:#9aa0a6; font-size:10px; font-weight:700'>AREA OF INTEREST</p>", unsafe_allow_html=True)
    lat_in = st.text_input("Lat", "40.4093", label_visibility="collapsed")
    lon_in = st.text_input("Lon", "49.8671", label_visibility="collapsed")
    
    if st.button("Zoom to Coordinate"):
        st.session_state.lat = float(lat_in)
        st.session_state.lon = float(lon_in)

    st.markdown("<br><p style='color:#9aa0a6; font-size:10px; font-weight:700'>RASTER DATA</p>", unsafe_allow_html=True)
    baseline = st.file_uploader("Baseline (T0)", type=["tif", "png", "jpg"], label_visibility="collapsed")
    current = st.file_uploader("Current (T1)", type=["tif", "png", "jpg"], label_visibility="collapsed")
    
    st.markdown("<div style='position:fixed; bottom:20px; color:#5f6368; font-size:10px;'>SATELLA v1.0 | AI Studio Clone</div>", unsafe_allow_html=True)

# --- ANA EKRAN (MAP) ---
col_map, col_metrics = st.columns([4.2, 1.2])

with col_map:
    # Live Monitoring Badge
    st.markdown("""
        <div style='position:absolute; top:20px; left:20px; z-index:1000; background:#111418; padding:6px 14px; border-radius:20px; border:1px solid #3c4043; color:white; font-size:11px; display:flex; align-items:center; gap:8px'>
            <span style='height:8px; width:8px; background:#ea4335; border-radius:50%'></span> LIVE MONITORING
        </div>
    """, unsafe_allow_html=True)
    
    l_val = st.session_state.get('lat', 40.4093)
    lo_val = st.session_state.get('lon', 49.8671)
    
    m = folium.Map([l_val, lo_val], zoom_start=15, tiles="CartoDB dark_matter", zoom_control=False)
    folium.Circle([l_val, lo_val], 200, color="#1a73e8", fill=True, opacity=0.3).add_to(m)
    folium_static(m, width=1450, height=900)

# --- SAĞ PANEL (METRICS) ---
with col_metrics:
    st.markdown("<p style='color:white; font-size:16px; font-weight:500; margin-bottom:20px'>System Metrics</p>", unsafe_allow_html=True)
    
    # Yeni Tikililər Box
    st.markdown("""
        <div style='display:flex; gap:10px'>
            <div class='metric-box' style='flex:1'><div class='metric-label'>New Structures</div><div class='metric-value'>6</div></div>
            <div class='metric-box' style='flex:1'><div class='metric-label'>Status</div><div class='metric-value' style='color:#3fb950; font-size:14px'>✓ Ready</div></div>
        </div>
    """, unsafe_allow_html=True)

    # Proqress Barlar
    metrics = [("Precision (IoU)", "92%", "#4285f4"), ("Recall Rate", "88%", "#34a853"), ("F1 Performance", "90%", "#a142f4")]
    for label, val, color in metrics:
        st.markdown(f"""
            <div class='progress-wrapper'>
                <div class='progress-text'><span>{label}</span><span>{val}</span></div>
                <div class='bar-bg'><div class='bar-fill' style='width:{val}; background:{color}'></div></div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("""
        <div class='warning-card'>
            <b>Verification Required</b><br>
            Changes detected in sensitive zones. Generated reports must be submitted to FHN for field verification.
        </div>
    """, unsafe_allow_html=True)

    if st.button("Generate FHN Report (PDF)"):
        pdf_data = generate_pdf(l_val, lo_val)
        st.download_button("Click to Download", pdf_data, "Satella_Report.pdf", use_container_width=True)
