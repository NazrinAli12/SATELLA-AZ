import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io

# 1. SAYFA AYARLARI
st.set_page_config(
    page_title="SATELLA AI", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. SESSION STATE BAŞLATMA
if 'lat' not in st.session_state:
    st.session_state.lat = 40.4093
if 'lon' not in st.session_state:
    st.session_state.lon = 49.8671
if 'is_analysed' not in st.session_state:
    st.session_state.is_analysed = False
if 't0' not in st.session_state:
    st.session_state.t0 = None
if 't1' not in st.session_state:
    st.session_state.t1 = None
if 'project_name' not in st.session_state:
    st.session_state.project_name = "Baku Urban Expansion"
if 'project_id' not in st.session_state:
    st.session_state.project_id = "AZ-BU-2025-09"

# 3. MINIMAL & SCI-FI CSS
st.markdown("""
<style>
    * { font-family: 'Courier New', monospace; }
    
    .stApp { 
        background-color: #000814;
        color: #e0e0e0;
    }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #0a0e27 !important;
        border-right: 2px solid #c41e3a !important;
    }

    /* MAIN CONTENT */
    [data-testid="stAppViewContainer"] {
        background-color: #000814;
    }

    /* TEXT COLOR */
    [data-testid="stSidebar"] * { 
        color: #c0c0c0 !important;
    }

    /* === HEADER === */
    .header-section {
        background: linear-gradient(135deg, #0d2b45 0%, #051a2e 100%);
        border: 1px solid #1a4d6d;
        border-radius: 2px;
        padding: 20px;
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }

    .header-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, #00d4ff, transparent);
    }

    .header-logo {
        font-size: 24px;
        font-weight: bold;
        letter-spacing: 3px;
        color: #00d4ff;
        margin: 0;
        text-transform: uppercase;
    }

    .header-subtitle {
        font-size: 8px;
        letter-spacing: 2px;
        color: #7a8fa0;
        margin: 8px 0 0 0;
        text-transform: uppercase;
    }

    .live-indicator {
        display: inline-block;
        margin-top: 10px;
        font-size: 9px;
        color: #00ff41;
        letter-spacing: 1px;
    }

    .live-indicator::before {
        content: '●';
        margin-right: 5px;
        animation: blink 1.5s infinite;
    }

    @keyframes blink {
        0%, 49%, 100% { opacity: 1; }
        50%, 99% { opacity: 0.3; }
    }

    /* === PROJECT CARD === */
    .project-section {
        background: #0a0e27;
        border: 1px solid #1a4d6d;
        border-radius: 2px;
        padding: 12px;
        margin-bottom: 20px;
    }

    .project-title {
        font-size: 13px;
        color: #00d4ff;
        margin: 0 0 8px 0;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .project-name {
        font-size: 13px;
        color: #e0e0e0;
        margin: 0;
        font-weight: bold;
    }

    .project-id {
        font-size: 9px;
        color: #7a8fa0;
        margin: 5px 0 0 0;
    }

    /* === SECTION TITLE === */
    .section-title {
        font-size: 9px;
        color: #7a8fa0;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 18px 0 10px 0;
        padding-bottom: 6px;
        border-bottom: 1px solid #1a4d6d;
    }

    .section-title-icon {
        color: #00d4ff;
        margin-right: 6px;
    }

    /* === INPUTS === */
    [data-testid="stSidebar"] .stTextInput input {
        background-color: #051a2e !important;
        border: 1px solid #1a4d6d !important;
        color: #e0e0e0 !important;
        border-radius: 1px !important;
        padding: 8px !important;
        font-size: 11px !important;
        font-family: 'Courier New', monospace !important;
    }

    [data-testid="stSidebar"] .stTextInput input:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 8px rgba(0, 212, 255, 0.1) !important;
    }

    /* === BUTTONS === */
    [data-testid="stSidebar"] .stButton button {
        background-color: #0d3f5a !important;
        color: #00d4ff !important;
        border: 1px solid #1a7a9f !important;
        border-radius: 1px !important;
        padding: 10px !important;
        font-size: 10px !important;
        font-weight: bold !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        transition: all 0.2s !important;
    }

    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #0f5a7f !important;
        border-color: #00d4ff !important;
        box-shadow: 0 0 12px rgba(0, 212, 255, 0.2) !important;
    }

    /* === FILE UPLOADER === */
    [data-testid="stSidebar"] .stFileUploader {
        margin: 8px 0;
    }

    .upload-box-label {
        font-size: 11px;
        color: #e0e0e0;
        margin-bottom: 4px;
        font-weight: bold;
    }

    .upload-box-info {
        font-size: 8px;
        color: #7a8fa0;
        margin-bottom: 6px;
    }

    /* === DIVIDER === */
    .divider {
        border: none;
        border-top: 1px solid #1a4d6d;
        margin: 15px 0;
    }

    /* === RIGHT PANEL === */
    .right-panel {
        background: #0a0e27;
        border: 2px solid #c41e3a;
        border-radius: 2px;
        padding: 15px;
        height: 100%;
    }

    .right-panel-title {
        font-size: 10px;
        color: #7a8fa0;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin: 0 0 15px 0;
        padding-bottom: 10px;
        border-bottom: 1px solid #1a4d6d;
    }

    /* === STATS === */
    .stat-box {
        background: #051a2e;
        border: 1px solid #1a4d6d;
        border-radius: 1px;
        padding: 12px;
        margin-bottom: 10px;
    }

    .stat-label {
        font-size: 8px;
        color: #7a8fa0;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stat-value {
        font-size: 20px;
        color: #00d4ff;
        margin: 8px 0 0 0;
        font-weight: bold;
    }

    .stat-secondary {
        font-size: 8px;
        color: #00ff41;
        margin: 6px 0 0 0;
    }

    /* === IMAGE FEED === */
    .image-feed-title {
        font-size: 9px;
        color: #7a8fa0;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 15px 0 10px 0;
        padding-bottom: 8px;
        border-bottom: 1px solid #1a4d6d;
    }

    .image-preview {
        background: #051a2e;
        border: 1px solid #1a4d6d;
        border-radius: 1px;
        padding: 8px;
        margin-bottom: 8px;
        text-align: center;
    }

    .image-preview-label {
        font-size: 8px;
        color: #00d4ff;
        margin: 0 0 6px 0;
        text-transform: uppercase;
    }

    .image-preview-img {
        width: 100%;
        border-radius: 1px;
        border: 1px solid #1a4d6d;
    }

    /* === EXPORT === */
    .export-section {
        margin-top: 15px;
        padding-top: 15px;
        border-top: 1px solid #1a4d6d;
    }

    .export-label {
        font-size: 8px;
        color: #7a8fa0;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
        display: block;
    }

    /* Main map container */
    .main-container {
        position: relative;
    }

</style>
""", unsafe_allow_html=True)

# 4. PDF GENERATOR
def create_report(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 12, "SATELLA AI - ANALYSIS REPORT", ln=True, align='C')
    pdf.ln(8)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f"Project: {st.session_state.project_name}", ln=True)
    pdf.cell(0, 8, f"Coordinates: {lat}, {lon}", ln=True)
    pdf.cell(0, 8, f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}", ln=True)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- SOL PANEL ---
with st.sidebar:
    # HEADER
    st.markdown("""
    <div class="header-section">
        <div class="header-logo">🛰️ SATELLA</div>
        <div class="header-subtitle">GEO-INTELLIGENCE PLATFORM</div>
        <div class="live-indicator">LIVE</div>
    </div>
    """, unsafe_allow_html=True)

    # PROJECT
    st.markdown('<div class="section-title"><span class="section-title-icon">▶</span>CURRENT PROJECT</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="project-section">
        <div class="project-name">{st.session_state.project_name}</div>
        <div class="project-id">ID: {st.session_state.project_id}</div>
    </div>
    """, unsafe_allow_html=True)

    # COORDINATES
    st.markdown('<div class="section-title"><span class="section-title-icon">🎯</span>TARGET COORDINATES</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div style="font-size: 7px; color: #7a8fa0; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">LATITUDE</div>', unsafe_allow_html=True)
        lat_val = st.text_input("LAT", value=str(st.session_state.lat), key="side_lat", label_visibility="collapsed")
    with col2:
        st.markdown('<div style="font-size: 7px; color: #7a8fa0; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px;">LONGITUDE</div>', unsafe_allow_html=True)
        lon_val = st.text_input("LON", value=str(st.session_state.lon), key="side_lon", label_visibility="collapsed")
    
    if st.button("🔄 Relocate Scanner", use_container_width=True):
        try:
            st.session_state.lat = float(lat_val)
            st.session_state.lon = float(lon_val)
            st.rerun()
        except:
            st.error("Invalid coordinates")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # INGEST ENGINE
    st.markdown('<div class="section-title"><span class="section-title-icon">⚙️</span>INGEST ENGINE</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="upload-box-label">📦 Baseline Imagery (T0)</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-box-info">Sentinel-2 L2A</div>', unsafe_allow_html=True)
    t0 = st.file_uploader("Upload baseline", type=["png", "jpg"], key="up_t0", label_visibility="collapsed")
    
    st.markdown('<div class="upload-box-label">▶️ Target Imagery (T1)</div>', unsafe_allow_html=True)
    st.markdown('<div class="upload-box-info">Sentinel-2 L2A</div>', unsafe_allow_html=True)
    t1 = st.file_uploader("Upload target", type=["png", "jpg"], key="up_t1", label_visibility="collapsed")

    if t0:
        st.session_state.t0 = t0
    if t1:
        st.session_state.t1 = t1

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # ANALYZE BUTTON
    if st.button("▶️ INITIALIZE AI ANALYSIS", use_container_width=True):
        if st.session_state.t0 and st.session_state.t1:
            st.session_state.is_analysed = True
            st.balloons()
            st.rerun()
        else:
            st.error("Upload both imagery files")

# --- MAIN LAYOUT ---
col_map, col_right = st.columns([3.2, 1.1])

with col_map:
    lat = st.session_state.lat
    lon = st.session_state.lon
    
    m = folium.Map(location=[lat, lon], zoom_start=18)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Satellite"
    ).add_to(m)
    folium.Marker([lat, lon], tooltip="Target Area", popup="Current Scan Zone").add_to(m)
    
    folium_static(m, width=1100, height=660)

with col_right:
    st.markdown("""
    <div class="right-panel">
        <div class="right-panel-title">🔍 DETECTION LAYER</div>
    </div>
    """, unsafe_allow_html=True)
    
    # STATS
    detected = "1" if st.session_state.is_analysed else "0"
    
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-label">Structural Detections</div>
        <div class="stat-value">{detected}</div>
    </div>
    <div class="stat-box">
        <div class="stat-label">AI Confidence</div>
        <div class="stat-value">92.4%</div>
        <div class="stat-secondary">Status: OPTIMAL</div>
    </div>
    """, unsafe_allow_html=True)
    
    # IMAGE FEED
    st.markdown('<div class="image-feed-title">📷 IMAGERY FEED</div>', unsafe_allow_html=True)
    
    if st.session_state.t0:
        st.markdown(f"""
        <div class="image-preview">
            <div class="image-preview-label">REF: 2024</div>
        </div>
        """, unsafe_allow_html=True)
        st.image(st.session_state.t0, use_container_width=True)
    
    if st.session_state.t1:
        st.markdown(f"""
        <div class="image-preview">
            <div class="image-preview-label">TARGET: 2025</div>
        </div>
        """, unsafe_allow_html=True)
        st.image(st.session_state.t1, use_container_width=True)
    
    # EXPORT
    if st.session_state.is_analysed:
        st.markdown("""
        <div class="export-section">
            <span class="export-label">📥 Export Protocol</span>
        </div>
        """, unsafe_allow_html=True)
        pdf_report = create_report(lat, lon)
        st.download_button(
            label="⬇️ Download Report",
            data=pdf_report,
            file_name=f"SATELLA_AZ-BU_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# FOOTER
st.markdown("""
<div style='position: fixed; bottom: 0; left: 0; right: 0; background: #000814; border-top: 1px solid #1a4d6d; padding: 12px; text-align: center;'>
<div style='font-size: 8px; color: #7a8fa0; letter-spacing: 1px;'>SATELLA AI v4.0 | GEOSPATIAL MONITORING SYSTEM</div>
<div style='font-size: 7px; color: #2a5a7a; margin-top: 4px;'>■ SYSTEM ONLINE  ■ AZEROSMOS LINK STEADY  ■ NO INTERFERENCE</div>
</div>
""", unsafe_allow_html=True)
