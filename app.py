import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
from PIL import Image

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

# 3. CSS AYARLARI (YENİ TASARIM)
st.markdown("""
<style>
    /* Ana fon */
    .stApp { background-color: #0b0d0e; }
    
    /* SIDEBAR STİLİ */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f1117 0%, #161b22 100%) !important;
        border-right: 1px solid #30363d !important;
    }
    
    [data-testid="stSidebar"] * { color: white !important; }

    /* HEADER LOGO BÖLÜMÜ */
    .sidebar-header {
        background: linear-gradient(135deg, #1f6feb 0%, #0d4fb8 100%);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        border: 1px solid #388bfd;
        text-align: center;
    }

    .sidebar-header h1 {
        margin: 0;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: 1px;
    }

    .sidebar-header p {
        margin: 5px 0 0 0;
        font-size: 9px;
        letter-spacing: 2px;
        opacity: 0.9;
        text-transform: uppercase;
    }

    .live-badge {
        display: inline-block;
        background: #28a745;
        color: white;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 8px;
        margin-top: 10px;
        font-weight: bold;
    }

    /* PROJECT CARD */
    .project-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-left: 3px solid #1f6feb;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
    }

    .project-card h3 {
        margin: 0 0 5px 0;
        font-size: 14px;
        color: white;
    }

    .project-card p {
        margin: 0;
        font-size: 11px;
        color: #8b949e;
    }

    /* SECTION BAŞLIKLARI */
    .section-title {
        font-size: 12px;
        font-weight: 700;
        color: #58a6ff;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 20px 0 12px 0;
        border-bottom: 1px solid #30363d;
        padding-bottom: 8px;
    }

    /* INPUT STYLES */
    [data-testid="stSidebar"] .stTextInput input {
        background-color: #0d1117 !important;
        border: 1px solid #30363d !important;
        color: #e6edf3 !important;
        border-radius: 6px !important;
        padding: 8px 12px !important;
        font-size: 13px !important;
    }

    [data-testid="stSidebar"] .stTextInput input:focus {
        border-color: #1f6feb !important;
        box-shadow: 0 0 0 3px rgba(31, 111, 235, 0.1) !important;
    }

    /* BUTTON STYLES */
    [data-testid="stSidebar"] .stButton button {
        background: linear-gradient(135deg, #1f6feb 0%, #0d4fb8 100%) !important;
        color: white !important;
        border: 1px solid #388bfd !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        padding: 10px !important;
        transition: all 0.3s !important;
    }

    [data-testid="stSidebar"] .stButton button:hover {
        background: linear-gradient(135deg, #0d4fb8 0%, #1f6feb 100%) !important;
        transform: translateY(-2px) !important;
    }

    /* FILE UPLOADER */
    [data-testid="stSidebar"] .stFileUploader {
        margin: 10px 0;
    }

    .upload-box {
        background: #0d1117;
        border: 2px dashed #30363d;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        margin: 8px 0;
        transition: all 0.3s;
    }

    .upload-box:hover {
        border-color: #1f6feb;
        background: #161b22;
    }

    /* ICON STYLES */
    .icon-badge {
        display: inline-block;
        width: 32px;
        height: 32px;
        background: #1f6feb;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        margin-right: 10px;
    }

    /* KOORDINAT INPUT WRAPPER */
    .coord-wrapper {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin: 10px 0;
    }

    /* METRIKA KARTLARI */
    .metric-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }

    .metric-label {
        color: #8b949e;
        font-size: 11px;
        margin: 0;
        text-transform: uppercase;
    }

    .metric-value {
        color: #58a6ff;
        font-size: 24px;
        font-weight: bold;
        margin: 5px 0 0 0;
    }

    /* DIVIDER */
    .divider {
        border: none;
        border-top: 1px solid #30363d;
        margin: 15px 0;
    }

</style>
""", unsafe_allow_html=True)

# 4. PDF GENERATOR
def create_report(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, "SATELLA AI - MONITORING REPORT", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Project: {st.session_state.project_name}", ln=True)
    pdf.cell(0, 10, f"Location: {lat}, {lon}", ln=True)
    pdf.cell(0, 10, f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- 🛰️ SOL PANEL (SIDEBAR) ---
with st.sidebar:
    # HEADER LOGO
    st.markdown("""
    <div class="sidebar-header">
        <h1>🛰️ SATELLA</h1>
        <p>GEO-INTELLIGENCE PLATFORM</p>
        <div class="live-badge">● LIVE</div>
    </div>
    """, unsafe_allow_html=True)

    # CURRENT PROJECT
    st.markdown('<div class="section-title">▶ CURRENT PROJECT</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="project-card">
        <h3>{st.session_state.project_name}</h3>
        <p>ID: {st.session_state.project_id}</p>
    </div>
    """, unsafe_allow_html=True)

    # TARGET COORDINATES
    st.markdown('<div class="section-title">🎯 TARGET COORDINATES</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        lat_val = st.text_input(
            "LATITUDE",
            value=str(st.session_state.lat),
            key="side_lat",
            label_visibility="collapsed"
        )
    with col2:
        lon_val = st.text_input(
            "LONGITUDE",
            value=str(st.session_state.lon),
            key="side_lon",
            label_visibility="collapsed"
        )
    
    if st.button("🔄 Relocate Scanner", use_container_width=True):
        try:
            st.session_state.lat = float(lat_val)
            st.session_state.lon = float(lon_val)
            st.success("📍 Coordinates updated!")
            st.rerun()
        except ValueError:
            st.error("Invalid coordinates")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # INGEST ENGINE
    st.markdown('<div class="section-title">⚙️ INGEST ENGINE</div>', unsafe_allow_html=True)
    
    st.markdown("**Baseline Imagery (T0)**")
    st.markdown("Sentinel-2 L2A")
    t0 = st.file_uploader("Upload T0 Image", type=["png", "jpg"], key="up_t0", label_visibility="collapsed")
    
    st.markdown("**Target Imagery (T1)**")
    st.markdown("Sentinel-2 L2A")
    t1 = st.file_uploader("Upload T1 Image", type=["png", "jpg"], key="up_t1", label_visibility="collapsed")

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
            st.success("✓ Analysis Complete")
            st.rerun()
        else:
            st.error("⚠️ Upload both images first")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # QUICK STATS
    st.markdown('<div class="section-title">📊 ANALYSIS STATS</div>', unsafe_allow_html=True)
    
    detected = "1" if st.session_state.is_analysed else "0"
    
    st.markdown(f"""
    <div class="metric-card">
        <p class="metric-label">DETECTED OBJECTS</p>
        <p class="metric-value">{detected}</p>
    </div>
    <div class="metric-card">
        <p class="metric-label">AI CONFIDENCE</p>
        <p class="metric-value">92.4%</p>
    </div>
    """, unsafe_allow_html=True)

# --- 🗺️ ƏSAS EKRAN LAYOUT ---
col_map, col_data = st.columns([3.5, 1.2])

with col_map:
    lat = st.session_state.lat
    lon = st.session_state.lon
    
    m = folium.Map(location=[lat, lon], zoom_start=18)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri Satellite",
        name="ArcGIS"
    ).add_to(m)
    folium.Marker([lat, lon], tooltip="Current Target Area").add_to(m)
    
    folium_static(m, width=1000, height=530)
    
    if st.session_state.t0 and st.session_state.t1:
        st.markdown("### 🔍 Side-by-Side Analysis")
        c1, c2 = st.columns(2)
        c1.image(st.session_state.t0, caption="2024 (T0)", use_container_width=True)
        c2.image(st.session_state.t1, caption="2025 (T1)", use_container_width=True)

with col_data:
    st.markdown("### 📊 Metrics")
    detected = "1" if st.session_state.is_analysed else "0"
    
    st.markdown(f"""
    <div class="metric-card">
        <p style="color:#8b949e; font-size:12px; margin:0;">NEW BUILDINGS</p>
        <p style="color:white; font-size:26px; font-weight:bold; margin:0;">{detected}</p>
    </div>
    <div class="metric-card">
        <p style="color:#8b949e; font-size:12px; margin:0;">CONFIDENCE</p>
        <p style="color:#58a6ff; font-size:26px; font-weight:bold; margin:0;">92.4%</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.is_analysed:
        st.info("✓ Analysis Ready")
        pdf_report = create_report(lat, lon)
        st.download_button(
            label="📥 DOWNLOAD REPORT",
            data=pdf_report,
            file_name=f"Satella_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.markdown("<br><hr><center style='color:#484f58; font-size:11px;'>SATELLA AI v3.3 | Professional Geospatial System</center>", unsafe_allow_html=True)
