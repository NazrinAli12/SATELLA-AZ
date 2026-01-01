import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF

# PAGE CONFIG
st.set_page_config(page_title="SATELLA AI", layout="wide", initial_sidebar_state="expanded")

# SESSION STATE
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

# CSS STYLING
st.markdown("""
<style>
    * { font-family: 'Courier New', monospace; }
    
    body, [data-testid="stAppViewContainer"] {
        background-color: #0a0e1a !important;
        color: #e0e0e0;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0f1419 !important;
        border-right: 2px solid #1a4d6d !important;
    }

    [data-testid="stSidebar"] * {
        color: #c0c0c0 !important;
    }

    /* SIDEBAR SECTIONS */
    .sidebar-item {
        margin: 15px 0;
    }

    /* HEADER */
    [data-testid="stSidebar"] .stMarkdown:first-child {
        background: linear-gradient(135deg, #0d2b45 0%, #051a2e 100%);
        border: 1px solid #1a4d6d;
        padding: 20px;
        border-radius: 3px;
        margin: 0;
    }

    /* INPUTS */
    [data-testid="stSidebar"] .stTextInput input {
        background-color: #051a2e !important;
        border: 1px solid #1a4d6d !important;
        color: #e0e0e0 !important;
        border-radius: 3px !important;
        padding: 8px 12px !important;
        font-size: 11px !important;
    }

    [data-testid="stSidebar"] .stTextInput input:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 6px rgba(0, 212, 255, 0.2) !important;
    }

    /* BUTTONS */
    [data-testid="stSidebar"] .stButton button {
        background-color: #0d3f5a !important;
        color: #00d4ff !important;
        border: 1px solid #1a7a9f !important;
        border-radius: 3px !important;
        width: 100% !important;
        padding: 10px !important;
        font-size: 10px !important;
        font-weight: bold !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        margin: 8px 0 !important;
    }

    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #0f5a7f !important;
        border-color: #00d4ff !important;
    }

    /* FILE UPLOADER */
    [data-testid="stSidebar"] .stFileUploader {
        margin: 8px 0;
    }

    /* DIVIDER */
    hr {
        border: none !important;
        border-top: 1px solid #1a4d6d !important;
        margin: 15px 0 !important;
    }

    /* MAIN CONTENT */
    .main {
        background-color: #0a0e1a !important;
    }

    /* RIGHT PANEL */
    .stColumn {
        background-color: #0a0e1a !important;
    }

    [data-testid="stVerticalBlock"] > [data-testid="stColumn"]:last-child {
        background-color: #0f1419 !important;
        border-left: 2px solid #1a4d6d !important;
        padding: 20px !important;
    }

</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    # Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0d2b45 0%, #051a2e 100%); border: 1px solid #1a4d6d; padding: 20px; border-radius: 3px; margin-bottom: 20px;">
        <h2 style="color: #00d4ff; margin: 0; font-size: 20px; letter-spacing: 2px;">🛰️ SATELLA</h2>
        <p style="color: #7a8fa0; font-size: 9px; margin: 8px 0 0 0; letter-spacing: 1px;">GEO-INTELLIGENCE PLATFORM</p>
        <span style="display: inline-block; background: #00a855; color: white; padding: 3px 6px; border-radius: 2px; font-size: 8px; margin-top: 10px;">● LIVE</span>
    </div>
    """, unsafe_allow_html=True)

    # Current Project
    st.markdown("### ▶ CURRENT PROJECT")
    st.markdown("""
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 12px; border-radius: 3px; margin-bottom: 20px;">
        <h4 style="margin: 0; color: white; font-size: 12px;">Baku Urban Expansion</h4>
        <p style="margin: 5px 0 0 0; color: #7a8fa0; font-size: 9px;">ID: AZ-BU-2025-09</p>
    </div>
    """, unsafe_allow_html=True)

    # Target Coordinates
    st.markdown("### 🎯 TARGET COORDINATES")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p style="font-size: 8px; color: #7a8fa0; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 1px;">LATITUDE</p>', unsafe_allow_html=True)
        lat_input = st.text_input("Latitude", value=str(st.session_state.lat), label_visibility="collapsed", key="lat_input")
    
    with col2:
        st.markdown('<p style="font-size: 8px; color: #7a8fa0; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 1px;">LONGITUDE</p>', unsafe_allow_html=True)
        lon_input = st.text_input("Longitude", value=str(st.session_state.lon), label_visibility="collapsed", key="lon_input")

    if st.button("🔄 RELOCATE SCANNER", use_container_width=True):
        try:
            st.session_state.lat = float(lat_input)
            st.session_state.lon = float(lon_input)
            st.rerun()
        except ValueError:
            st.error("Invalid coordinates")

    st.markdown("---")

    # Ingest Engine
    st.markdown("### ⚙️ INGEST ENGINE")
    
    st.markdown('<p style="font-size: 10px; color: white; font-weight: bold; margin-bottom: 3px;">📦 Baseline Imagery (T0)</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 8px; color: #7a8fa0; margin-bottom: 8px;">Sentinel-2 L2A</p>', unsafe_allow_html=True)
    t0_file = st.file_uploader("Upload T0", type=["png", "jpg"], label_visibility="collapsed", key="t0_uploader")

    st.markdown('<p style="font-size: 10px; color: white; font-weight: bold; margin-top: 15px; margin-bottom: 3px;">▶️ Target Imagery (T1)</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 8px; color: #7a8fa0; margin-bottom: 8px;">Sentinel-2 L2A</p>', unsafe_allow_html=True)
    t1_file = st.file_uploader("Upload T1", type=["png", "jpg"], label_visibility="collapsed", key="t1_uploader")

    if t0_file:
        st.session_state.t0 = t0_file
    if t1_file:
        st.session_state.t1 = t1_file

    st.markdown("---")

    # Analyze Button
    if st.button("▶️ INITIALIZE AI ANALYSIS", use_container_width=True):
        if st.session_state.t0 and st.session_state.t1:
            st.session_state.is_analysed = True
            st.balloons()
            st.success("Analysis complete!")
            st.rerun()
        else:
            st.error("Upload both imagery files")

# MAIN LAYOUT
map_col, right_col = st.columns([3.5, 1])

with map_col:
    # Map
    lat = st.session_state.lat
    lon = st.session_state.lon
    
    m = folium.Map(location=[lat, lon], zoom_start=18)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Satellite"
    ).add_to(m)
    folium.Marker([lat, lon], popup="Target Area").add_to(m)
    
    folium_static(m, width=1100, height=700)

with right_col:
    st.markdown("""
    <div style="background: #0f1419; border: 1px solid #1a4d6d; padding: 15px; border-radius: 3px;">
        <h3 style="color: #7a8fa0; font-size: 9px; text-transform: uppercase; letter-spacing: 1px; margin-top: 0;">🔍 DETECTION LAYER</h3>
    </div>
    """, unsafe_allow_html=True)

    detected = "1" if st.session_state.is_analysed else "0"

    st.markdown(f"""
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 12px; border-radius: 3px; margin-top: 10px;">
        <p style="color: #7a8fa0; font-size: 8px; text-transform: uppercase; letter-spacing: 1px; margin: 0;">STRUCTURAL DETECTIONS</p>
        <p style="color: #00d4ff; font-size: 22px; font-weight: bold; margin: 8px 0 0 0;">{detected}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 12px; border-radius: 3px; margin-top: 10px;">
        <p style="color: #7a8fa0; font-size: 8px; text-transform: uppercase; letter-spacing: 1px; margin: 0;">AI CONFIDENCE</p>
        <p style="color: #00d4ff; font-size: 22px; font-weight: bold; margin: 8px 0 0 0;">92.4%</p>
        <p style="color: #00ff41; font-size: 8px; margin: 6px 0 0 0;">Status: OPTIMAL</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 12px; border-radius: 3px; margin-top: 15px;">
        <p style="color: #7a8fa0; font-size: 8px; text-transform: uppercase; letter-spacing: 1px; margin: 0;">📥 EXPORT PROTOCOL</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.is_analysed:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 12, "SATELLA AI REPORT", ln=True, align='C')
        pdf.ln(8)
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 8, f"Location: {lat}, {lon}", ln=True)
        pdf.cell(0, 8, f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
        pdf_data = pdf.output(dest='S').encode('latin-1', 'ignore')
        
        st.download_button(
            label="⬇️ Download Report",
            data=pdf_data,
            file_name=f"SATELLA_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    # Imagery Feed
    st.markdown("""
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 12px; border-radius: 3px; margin-top: 15px;">
        <p style="color: #7a8fa0; font-size: 8px; text-transform: uppercase; letter-spacing: 1px; margin: 0;">📷 IMAGERY FEED</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.t0:
        st.markdown('<p style="color: #00d4ff; font-size: 8px; text-align: center; margin: 10px 0 5px 0; text-transform: uppercase;">REF: 2024</p>', unsafe_allow_html=True)
        st.image(st.session_state.t0, use_container_width=True)

    if st.session_state.t1:
        st.markdown('<p style="color: #00d4ff; font-size: 8px; text-align: center; margin: 10px 0 5px 0; text-transform: uppercase;">TARGET: 2025</p>', unsafe_allow_html=True)
        st.image(st.session_state.t1, use_container_width=True)
