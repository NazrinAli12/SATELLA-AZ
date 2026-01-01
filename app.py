import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF

# 1. SAYFA AYARLARI
st.set_page_config(
    page_title="SATELLA AI", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. SESSION STATE
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

# 3. GLOBAL CSS
st.markdown("""
<style>
    * { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Courier New', monospace; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #0a0e27 !important;
        color: #e0e0e0;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #050814 !important;
        border-right: 1px solid #2a4a6a !important;
    }

    [data-testid="stSidebarContent"] {
        padding: 0 !important;
    }

    /* REMOVE DEFAULT PADDING */
    .stContainer { padding: 0 !important; }
    
    /* MAIN PADDING */
    .main { padding: 0 !important; }

    /* === SIDEBAR STYLING === */
    [data-testid="stSidebar"] * {
        color: #c0c0c0 !important;
    }

    .sidebar-item {
        padding: 10px;
        margin: 5px 0;
        border-radius: 4px;
    }

    /* Header */
    .sidebar-header {
        padding: 20px;
        border-bottom: 1px solid #2a4a6a;
    }

    .sidebar-header h1 {
        margin: 0;
        font-size: 18px;
        font-weight: bold;
        color: white;
        letter-spacing: 1px;
    }

    .sidebar-header p {
        margin: 5px 0 0 0;
        font-size: 10px;
        color: #7a8fa0;
        letter-spacing: 1px;
    }

    .live-badge {
        display: inline-block;
        background: #00a855;
        color: white;
        padding: 3px 6px;
        border-radius: 2px;
        font-size: 8px;
        margin-top: 8px;
        font-weight: bold;
    }

    /* Section Titles */
    .section-title {
        padding: 15px 20px 8px 20px;
        font-size: 10px;
        color: #7a8fa0;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 10px;
        border-bottom: 1px solid #2a4a6a;
    }

    /* Project Card */
    .project-card {
        background: #0a0e27;
        border: 1px solid #2a4a6a;
        margin: 0 15px;
        padding: 12px;
        border-radius: 3px;
    }

    .project-card h3 {
        margin: 0;
        font-size: 12px;
        color: white;
        font-weight: bold;
    }

    .project-card p {
        margin: 5px 0 0 0;
        font-size: 9px;
        color: #7a8fa0;
    }

    /* Input Container */
    .input-group {
        padding: 0 15px;
    }

    .input-label {
        font-size: 8px;
        color: #7a8fa0;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 4px;
        display: block;
    }

    [data-testid="stSidebar"] .stTextInput input {
        background-color: #0a0e27 !important;
        border: 1px solid #2a4a6a !important;
        color: #e0e0e0 !important;
        border-radius: 3px !important;
        padding: 8px !important;
        font-size: 11px !important;
    }

    [data-testid="stSidebar"] .stTextInput input:focus {
        border-color: #00d4ff !important;
    }

    /* Buttons */
    [data-testid="stSidebar"] .stButton button {
        background-color: #0d3f5a !important;
        color: #00d4ff !important;
        border: 1px solid #1a7a9f !important;
        border-radius: 3px !important;
        padding: 10px 15px !important;
        font-size: 10px !important;
        font-weight: bold !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        width: 100% !important;
        margin: 8px 15px !important;
    }

    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #0f5a7f !important;
        border-color: #00d4ff !important;
    }

    /* File Uploader */
    [data-testid="stSidebar"] .stFileUploader {
        margin: 8px 15px !important;
    }

    .upload-label {
        font-size: 11px;
        color: white;
        font-weight: bold;
        margin-bottom: 3px;
        display: block;
    }

    .upload-info {
        font-size: 8px;
        color: #7a8fa0;
        margin-bottom: 8px;
        display: block;
    }

    /* === MAIN CONTENT === */
    .top-bar {
        background: #050814;
        border-bottom: 1px solid #2a4a6a;
        padding: 15px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .search-box {
        flex: 1;
        background: #0a0e27;
        border: 1px solid #2a4a6a;
        padding: 10px 15px;
        border-radius: 3px;
        color: #7a8fa0;
        font-size: 10px;
    }

    .sat-link {
        margin-left: 20px;
        font-size: 9px;
        color: #7a8fa0;
    }

    .sat-link-status {
        color: #00d4ff;
        font-weight: bold;
    }

    /* Right Panel */
    .right-panel {
        background: #050814;
        border-left: 1px solid #2a4a6a;
        padding: 20px;
        height: auto;
        min-width: 350px;
    }

    .panel-title {
        font-size: 10px;
        color: #7a8fa0;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid #2a4a6a;
    }

    .data-box {
        background: #0a0e27;
        border: 1px solid #2a4a6a;
        padding: 12px;
        margin-bottom: 10px;
        border-radius: 3px;
    }

    .data-label {
        font-size: 9px;
        color: #7a8fa0;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 6px;
    }

    .data-value {
        font-size: 22px;
        color: #00d4ff;
        font-weight: bold;
        margin: 0;
    }

    .data-status {
        font-size: 8px;
        color: #00ff41;
        margin-top: 6px;
    }

    .image-preview-box {
        background: #0a0e27;
        border: 1px dashed #2a4a6a;
        padding: 8px;
        margin-bottom: 8px;
        border-radius: 3px;
        text-align: center;
    }

    .image-label {
        font-size: 8px;
        color: #00d4ff;
        margin-bottom: 6px;
        text-transform: uppercase;
    }

    /* Bottom Timeline */
    .timeline-section {
        background: #050814;
        border-top: 1px solid #2a4a6a;
        padding: 15px 20px;
        font-size: 9px;
        color: #7a8fa0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .timeline-label {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .timeline-dot {
        width: 8px;
        height: 8px;
        background: #00d4ff;
        border-radius: 50%;
    }

    /* Footer */
    .footer-bar {
        background: #050814;
        border-top: 1px solid #2a4a6a;
        padding: 12px 20px;
        text-align: right;
        font-size: 8px;
        color: #7a8fa0;
    }

</style>
""", unsafe_allow_html=True)

# PDF GENERATOR
def create_report(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 12, "SATELLA AI - ANALYSIS REPORT", ln=True, align='C')
    pdf.ln(8)
    pdf.set_font("Arial", '', 10)
    pdf.cell(0, 8, f"Location: {lat}, {lon}", ln=True)
    pdf.cell(0, 8, f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}", ln=True)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# ===== SIDEBAR =====
with st.sidebar:
    # Header
    st.markdown("""
    <div class="sidebar-header">
        <h1>🛰️ SATELLA</h1>
        <p>GEO-INTELLIGENCE PLATFORM</p>
        <div class="live-badge">● LIVE</div>
    </div>
    """, unsafe_allow_html=True)

    # Project Section
    st.markdown('<div class="section-title">▶ CURRENT PROJECT</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="project-card">
        <h3>Baku Urban Expansion</h3>
        <p>ID: AZ-BU-2025-09</p>
    </div>
    """, unsafe_allow_html=True)

    # Coordinates Section
    st.markdown('<div class="section-title">🎯 TARGET COORDINATES</div>', unsafe_allow_html=True)
    st.markdown('<div class="input-group">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<span class="input-label">LATITUDE</span>', unsafe_allow_html=True)
        lat_val = st.text_input("LAT", value=str(st.session_state.lat), key="side_lat", label_visibility="collapsed")
    with col2:
        st.markdown('<span class="input-label">LONGITUDE</span>', unsafe_allow_html=True)
        lon_val = st.text_input("LON", value=str(st.session_state.lon), key="side_lon", label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🔄 Relocate Scanner"):
        try:
            st.session_state.lat = float(lat_val)
            st.session_state.lon = float(lon_val)
            st.rerun()
        except:
            st.error("Invalid coordinates")

    # Ingest Engine
    st.markdown('<div class="section-title">⚙️ INGEST ENGINE</div>', unsafe_allow_html=True)
    st.markdown('<div class="input-group">', unsafe_allow_html=True)
    
    st.markdown('<span class="upload-label">📦 Baseline Imagery (T0)</span>', unsafe_allow_html=True)
    st.markdown('<span class="upload-info">Sentinel-2 L2A</span>', unsafe_allow_html=True)
    t0 = st.file_uploader("Upload T0", type=["png", "jpg"], key="up_t0", label_visibility="collapsed")
    
    st.markdown('<span class="upload-label" style="margin-top: 10px;">▶️ Target Imagery (T1)</span>', unsafe_allow_html=True)
    st.markdown('<span class="upload-info">Sentinel-2 L2A</span>', unsafe_allow_html=True)
    t1 = st.file_uploader("Upload T1", type=["png", "jpg"], key="up_t1", label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)

    if t0:
        st.session_state.t0 = t0
    if t1:
        st.session_state.t1 = t1

    # Analyze Button
    if st.button("▶️ INITIALIZE AI ANALYSIS"):
        if st.session_state.t0 and st.session_state.t1:
            st.session_state.is_analysed = True
            st.balloons()
            st.rerun()
        else:
            st.error("Upload both imagery files")

# ===== MAIN LAYOUT =====
# Top Bar
st.markdown("""
<div class="top-bar">
    <input type="text" class="search-box" placeholder="🔍 Search coordinates, projects, or inspectors..." />
    <div class="sat-link">SAT LINK: <span class="sat-link-status">ENCRYPTED</span></div>
</div>
""", unsafe_allow_html=True)

main_col, right_col = st.columns([4, 1.2])

with main_col:
    lat = st.session_state.lat
    lon = st.session_state.lon
    
    # Map
    m = folium.Map(location=[lat, lon], zoom_start=18)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Satellite"
    ).add_to(m)
    folium.Marker([lat, lon], popup="Target Area").add_to(m)
    
    folium_static(m, width=1200, height=650)

with right_col:
    st.markdown("""
    <div class="right-panel">
        <div class="panel-title">🔍 DETECTION LAYER</div>
    </div>
    """, unsafe_allow_html=True)
    
    detected = "1" if st.session_state.is_analysed else "0"
    
    st.markdown(f"""
    <div class="data-box">
        <div class="data-label">Structural Detections</div>
        <div class="data-value">{detected}</div>
    </div>
    <div class="data-box">
        <div class="data-label">AI Confidence</div>
        <div class="data-value">92.4%</div>
        <div class="data-status">✓ Status: OPTIMAL</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #2a4a6a;"><div class="data-label">📥 EXPORT PROTOCOL</div></div>', unsafe_allow_html=True)
    
    if st.session_state.is_analysed:
        pdf_report = create_report(lat, lon)
        st.download_button(
            label="⬇️ Download Report",
            data=pdf_report,
            file_name=f"SATELLA_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    # Imagery Feed
    st.markdown('<div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid #2a4a6a;"><div class="data-label">📷 IMAGERY FEED</div></div>', unsafe_allow_html=True)
    
    if st.session_state.t0:
        st.markdown('<div class="image-preview-box"><div class="image-label">REF: 2024</div></div>', unsafe_allow_html=True)
        st.image(st.session_state.t0, use_container_width=True)
    
    if st.session_state.t1:
        st.markdown('<div class="image-preview-box"><div class="image-label">TARGET: 2025</div></div>', unsafe_allow_html=True)
        st.image(st.session_state.t1, use_container_width=True)

# Timeline Section
st.markdown("""
<div class="timeline-section">
    <div style="flex: 1;">
        <span style="color: #00d4ff; font-weight: bold;">TEMPORAL TIMELINE</span>
        <div style="margin-top: 8px; background: #0a0e27; height: 4px; border-radius: 2px; margin-right: 20px;">
            <div style="background: #00d4ff; height: 100%; width: 50%; border-radius: 2px;"></div>
        </div>
    </div>
    <div style="text-align: right;">
        <div style="font-size: 9px; color: #7a8fa0; margin-bottom: 6px;">SELECTED RANGE</div>
        <div style="font-size: 11px; color: #e0e0e0; font-weight: bold;">APR 2024 — JAN 2025</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer-bar">
    <span style="margin-right: 20px;">■ SYSTEM ONLINE</span>
    <span style="margin-right: 20px;">■ AZEROSMOS LINK STEADY</span>
    <span style="margin-right: 20px;">■ NO INTERFERENCE</span>
    | AZERBAIJAN MARITIME SECTOR v4.2 | SATELLA INTELLIGENCE 2025
</div>
""", unsafe_allow_html=True)
