import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io

# 1. Page Config
st.set_page_config(page_title="SATELLA AI", layout="wide", initial_sidebar_state="expanded")

# 2. CSS: No-Scroll, Fixed Panels, Compact Sidebar
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], .main {
        font-family: 'Inter', sans-serif;
        background-color: #0b0d0e !important;
        overflow: hidden !important;
        margin: 0; padding: 0;
    }

    /* Sidebars and Header hide */
    [data-testid="stHeader"] { display: none; }
    
    /* LEFT SIDEBAR - 360px Compact */
    section[data-testid="stSidebar"] {
        width: 360px !important;
        background-color: #111418 !important;
        border-right: 1px solid #2d333b !important;
    }
    section[data-testid="stSidebar"] > div {
        height: 100vh !important;
        overflow: hidden !important;
        padding: 1rem !important;
    }

    /* RIGHT PANEL - Metrics */
    [data-testid="column"]:nth-child(2) {
        background-color: #111418 !important;
        border-left: 1px solid #2d333b !important;
        padding: 20px !important;
        height: 100vh;
        position: fixed; right: 0; top: 0;
    }

    /* Gap and Padding control */
    .stVerticalBlock { gap: 0.3rem !important; }
    div[data-testid="stFileUploader"] { margin-bottom: -10px; }

    /* UI Elements */
    div.stButton > button {
        background: #1a73e8 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        height: 38px !important;
        width: 100%;
    }
    .m-box {
        background: #1a1f24;
        border: 1px solid #3c4043;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# 3. PDF Generator
def generate_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "SATELLA ANALYSIS REPORT", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Coordinates: {lat}, {lon}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1e3a8a,#3b82f6);padding:1rem;border-radius:10px;margin-bottom:1rem'>
        <h2 style='color:white;margin:0;font-size:20px;'>🛰️ SATELLA</h2>
        <p style='color:#bfdbfe;margin:0;font-size:11px'>Enterprise AI Monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-size:11px; font-weight:700; color:#9ca3af; margin-bottom:2px'>LOCATION</p>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a: lat_in = st.text_input("Lat", value="40.461023", label_visibility="collapsed", key="l1")
    with col_b: lon_in = st.text_input("Lon", value="49.889897", label_visibility="collapsed", key="l2")
    
    if st.button("🎯 SYNC MAP"):
        st.session_state.lat = float(lat_in)
        st.session_state.lon = float(lon_in)
        st.rerun()

    st.markdown("<p style='font-size:11px; font-weight:700; color:#9ca3af; margin-top:10px; margin-bottom:2px'>DATA SOURCE</p>", unsafe_allow_html=True)
    t0_file = st.file_uploader("T0", type=["png","jpg","tif"], key="t0_up", label_visibility="collapsed")
    t1_file = st.file_uploader("T1", type=["png","jpg","tif"], key="t1_up", label_visibility="collapsed")
    
    if st.button("🚀 RUN ANALYSIS"):
        if t0_file and t1_file: st.session_state.run = True
        else: st.warning("Upload both images.")

# --- MAIN CONTENT ---
c_map, c_metric = st.columns([3.8, 1.2])

with c_map:
    # Koordinatları session-dan alırıq
    cur_lat = st.session_state.get('lat', 40.461023)
    cur_lon = st.session_state.get('lon', 49.889897)
    
    # FOLIUM XƏTASI ÜÇÜN ABSOLUT HƏLL:
    # 'tiles' parametrini Map daxilində deyil, ayrıca TileLayer daxilində veririk.
    m = folium.Map(location=[cur_lat, cur_lon], zoom_start=18, tiles=None)
    
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        name="Satellite View",
        overlay=False,
        control=True
    ).add_to(m)
    
    folium.Marker([cur_lat, cur_lon], icon=folium.Icon(color="red", icon="info-sign")).add_to(m)
    
    # Xəritəni göstər
    folium_static(m, width=1200, height=620)
    
    # Şəkillər (Xəritənin dərhal altında)
    if t0_file or t1_file:
        st.markdown("<br>", unsafe_allow_html=True)
        im_col1, im_col2 = st.columns(2)
        with im_col1:
            if t0_file: st.image(t0_file, caption="Baseline 2024", use_container_width=True)
        with im_col2:
            if t1_file: st.image(t1_file, caption="Current 2025", use_container_width=True)

with c_metric:
    st.markdown("### 📊 Metrics")
    st.markdown(f"""
    <div class="m-box">
        <p style='color:#9ca3af;font-size:10px;font-weight:700;margin:0'>DETECTED STRUCTURES</p>
        <p style='color:white;font-size:26px;font-weight:800;margin:0'>6</p>
    </div>
    <div class="m-box">
        <p style='color:#9ca3af;font-size:10px;font-weight:700;margin:0'>AI CONFIDENCE</p>
        <p style='color:#10b981;font-size:26px;font-weight:800;margin:0'>92.4%</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get('run', False):
        pdf = generate_pdf(cur_lat, cur_lon)
        st.download_button("📄 DOWNLOAD REPORT", data=pdf, file_name="satella_report.pdf", use_container_width=True)

    st.markdown("<div style='position:fixed; bottom:20px; color:#4b5563; font-size:10px;'>SATELLA ENGINE v3.2</div>", unsafe_allow_html=True)
