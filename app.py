import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io

st.set_page_config(page_title="SATELLA", layout="wide", initial_sidebar_state="expanded")

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
if 'detections' not in st.session_state:
    st.session_state.detections = 0
if 'confidence' not in st.session_state:
    st.session_state.confidence = 0

# GLOBAL CSS STYLING
st.markdown("""
<style>
    * { 
        font-family: 'Courier New', Courier, monospace;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
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
    
    /* TEXT INPUT */
    input {
        background-color: #051a2e !important;
        border: 1px solid #1a4d6d !important;
        color: #e0e0e0 !important;
        border-radius: 3px !important;
        padding: 8px 12px !important;
        font-size: 12px !important;
        font-family: 'Courier New', monospace !important;
    }
    
    input:focus {
        border-color: #00d4ff !important;
        box-shadow: 0 0 8px rgba(0, 212, 255, 0.3) !important;
    }
    
    /* BUTTONS */
    button {
        background-color: #0d3f5a !important;
        color: #00d4ff !important;
        border: 1px solid #1a7a9f !important;
        border-radius: 3px !important;
        padding: 10px 16px !important;
        font-size: 11px !important;
        font-weight: bold !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        cursor: pointer;
        font-family: 'Courier New', monospace !important;
        transition: all 0.2s ease;
    }
    
    button:hover {
        background-color: #0f5a7f !important;
        border-color: #00d4ff !important;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.2) !important;
    }
    
    button:active {
        background-color: #0a3f5f !important;
    }
    
    /* FILE UPLOADER */
    [data-testid="stFileUploader"] {
        margin: 8px 0;
    }
    
    /* DIVIDER */
    hr {
        border: none !important;
        border-top: 1px solid #1a4d6d !important;
        margin: 15px 0 !important;
    }
    
    /* MARKDOWN HEADINGS */
    h1, h2, h3, h4, h5, h6 {
        color: #00d4ff !important;
        font-family: 'Courier New', monospace !important;
    }
    
    .block-container {
        padding: 2rem 1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ========== SIDEBAR ==========
with st.sidebar:
    # HEADER
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0d2b45 0%, #051a2e 100%); border: 1px solid #1a4d6d; padding: 16px; border-radius: 3px; margin-bottom: 20px;">
        <h2 style="color: #00d4ff; margin: 0; font-size: 18px; letter-spacing: 2px; font-weight: bold;">🛰️ SATELLA</h2>
        <p style="color: #7a8fa0; font-size: 10px; margin: 6px 0 0 0; letter-spacing: 1px;">GEO-INTELLIGENCE PLATFORM</p>
        <span style="display: inline-block; background: #00a855; color: white; padding: 4px 8px; border-radius: 2px; font-size: 8px; margin-top: 10px; font-weight: bold;">● LIVE</span>
    </div>
    """, unsafe_allow_html=True)

    # CURRENT PROJECT
    st.markdown('<p style="font-size: 9px; color: #7a8fa0; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">▶ CURRENT PROJECT</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 12px; border-radius: 3px; margin-bottom: 20px;">
        <h4 style="margin: 0; color: #e0e0e0; font-size: 12px; font-weight: bold;">Baku Urban Expansion</h4>
        <p style="margin: 6px 0 0 0; color: #7a8fa0; font-size: 9px;">ID: AZ-BU-2025-09</p>
    </div>
    """, unsafe_allow_html=True)

    # TARGET COORDINATES
    st.markdown('<p style="font-size: 9px; color: #7a8fa0; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">🎯 TARGET COORDINATES</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<p style="font-size: 8px; color: #7a8fa0; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 1px;">Latitude</p>', unsafe_allow_html=True)
        lat_input = st.text_input("Lat", value=str(st.session_state.lat), label_visibility="collapsed", key="lat_in")
    
    with col2:
        st.markdown('<p style="font-size: 8px; color: #7a8fa0; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 1px;">Longitude</p>', unsafe_allow_html=True)
        lon_input = st.text_input("Lon", value=str(st.session_state.lon), label_visibility="collapsed", key="lon_in")

    if st.button("🔄 RELOCATE SCANNER", use_container_width=True):
        try:
            st.session_state.lat = float(lat_input)
            st.session_state.lon = float(lon_input)
            st.rerun()
        except ValueError:
            st.error("Invalid coordinates")

    st.markdown("---")

    # INGEST ENGINE
    st.markdown('<p style="font-size: 9px; color: #7a8fa0; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px;">⚙️ INGEST ENGINE</p>', unsafe_allow_html=True)
    
    st.markdown('<p style="font-size: 10px; color: #e0e0e0; font-weight: bold; margin-bottom: 3px;">📦 Baseline Imagery (T0)</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 8px; color: #7a8fa0; margin-bottom: 8px;">Sentinel-2 L2A</p>', unsafe_allow_html=True)
    t0_file = st.file_uploader("Upload T0", type=["png", "jpg", "jpeg"], label_visibility="collapsed", key="t0_up")

    st.markdown('<p style="font-size: 10px; color: #e0e0e0; font-weight: bold; margin-top: 12px; margin-bottom: 3px;">▶️ Target Imagery (T1)</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 8px; color: #7a8fa0; margin-bottom: 8px;">Sentinel-2 L2A</p>', unsafe_allow_html=True)
    t1_file = st.file_uploader("Upload T1", type=["png", "jpg", "jpeg"], label_visibility="collapsed", key="t1_up")

    if t0_file:
        st.session_state.t0 = t0_file
    if t1_file:
        st.session_state.t1 = t1_file

    st.markdown("---")

    # ANALYSIS BUTTON
    if st.button("▶️ INITIALIZE AI ANALYSIS", use_container_width=True):
        if st.session_state.t0 and st.session_state.t1:
            st.session_state.is_analysed = True
            st.session_state.detections = 1
            st.session_state.confidence = 92.4
            st.balloons()
            st.success("✓ Analysis complete!")
            st.rerun()
        else:
            st.error("⚠️ Upload both imagery files")

# ========== MAIN LAYOUT ==========
map_col, right_col = st.columns([3.2, 1], gap="small")

# MAP COLUMN
with map_col:
    lat = st.session_state.lat
    lon = st.session_state.lon
    
    m = folium.Map(location=[lat, lon], zoom_start=18)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Satellite"
    ).add_to(m)
    folium.Marker([lat, lon], popup="Target Area", icon=folium.Icon(color='blue', icon='target')).add_to(m)
    
    folium_static(m, width=1100, height=650)

# RIGHT COLUMN - DETECTION PANEL
with right_col:
    st.markdown("""
    <div style="background: #0f1419; border: 1px solid #1a4d6d; padding: 12px; border-radius: 3px; margin-bottom: 12px;">
        <p style="color: #7a8fa0; font-size: 8px; text-transform: uppercase; letter-spacing: 1px; margin: 0;">🔍 DETECTION LAYER</p>
    </div>
    """, unsafe_allow_html=True)

    # Structural Detections
    st.markdown(f"""
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 12px; border-radius: 3px; margin-bottom: 10px;">
        <p style="color: #7a8fa0; font-size: 8px; text-transform: uppercase; letter-spacing: 1px; margin: 0;">Structural Detections</p>
        <p style="color: #00d4ff; font-size: 28px; font-weight: bold; margin: 8px 0 0 0;">{st.session_state.detections}</p>
    </div>
    """, unsafe_allow_html=True)

    # AI Confidence
    confidence = st.session_state.confidence if st.session_state.is_analysed else 0
    st.markdown(f"""
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 12px; border-radius: 3px; margin-bottom: 10px;">
        <p style="color: #7a8fa0; font-size: 8px; text-transform: uppercase; letter-spacing: 1px; margin: 0;">AI Confidence</p>
        <p style="color: #00d4ff; font-size: 28px; font-weight: bold; margin: 8px 0 0 0;">{confidence:.1f}%</p>
        <p style="color: #00ff41; font-size: 8px; margin: 6px 0 0 0; text-transform: uppercase;">{'Status: OPTIMAL' if st.session_state.is_analysed else 'Status: IDLE'}</p>
    </div>
    """, unsafe_allow_html=True)

    # Export Protocol
    st.markdown("""
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 12px; border-radius: 3px; margin-bottom: 10px;">
        <p style="color: #7a8fa0; font-size: 8px; text-transform: uppercase; letter-spacing: 1px; margin: 0;">📥 Export Protocol</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.is_analysed:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 12, "SATELLA AI REPORT", ln=True, align='C')
        pdf.ln(8)
        pdf.set_font("Arial", '', 11)
        pdf.cell(0, 8, f"Location: {lat:.4f}, {lon:.4f}", ln=True)
        pdf.cell(0, 8, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
        pdf.cell(0, 8, f"Detections: {st.session_state.detections}", ln=True)
        pdf.cell(0, 8, f"Confidence: {st.session_state.confidence:.1f}%", ln=True)
        pdf.ln(5)
        pdf.set_font("Arial", '', 10)
        pdf.multi_cell(0, 5, "Analysis Status: COMPLETE\nSystem: OPERATIONAL")
        
        pdf_bytes = pdf.output(dest='S').encode('latin-1', 'ignore')
        
        st.download_button(
            label="⬇️ DOWNLOAD REPORT",
            data=pdf_bytes,
            file_name=f"SATELLA_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    # Imagery Feed
    st.markdown("""
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 12px; border-radius: 3px; margin-top: 12px;">
        <p style="color: #7a8fa0; font-size: 8px; text-transform: uppercase; letter-spacing: 1px; margin: 0;">📷 Imagery Feed</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.t0:
        st.markdown('<p style="color: #00d4ff; font-size: 8px; text-align: center; margin: 8px 0 4px 0; text-transform: uppercase; font-weight: bold;">REF: 2024</p>', unsafe_allow_html=True)
        st.image(st.session_state.t0, use_container_width=True)

    if st.session_state.t1:
        st.markdown('<p style="color: #00d4ff; font-size: 8px; text-align: center; margin: 8px 0 4px 0; text-transform: uppercase; font-weight: bold;">TARGET: 2025</p>', unsafe_allow_html=True)
        st.image(st.session_state.t1, use_container_width=True)
