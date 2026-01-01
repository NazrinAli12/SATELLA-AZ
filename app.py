import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF

st.set_page_config(page_title="SATELLA", layout="wide", initial_sidebar_state="expanded")

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

st.markdown("""
<style>
    * { font-family: 'Courier New', monospace; }
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0a0e1a !important;
        color: #c0c0c0;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0f1419 !important;
        border-right: 3px solid #d946a6 !important;
        padding-top: 0 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    
    .sidebar-icon-row {
        display: flex;
        gap: 12px;
        margin-bottom: 30px;
        padding-left: 8px;
    }
    
    .sidebar-icon {
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #051a2e;
        border: 1px solid #1a4d6d;
        border-radius: 4px;
        color: #00d4ff;
        font-size: 18px;
        cursor: pointer;
    }
    
    .section-title {
        color: #00d4ff;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: bold;
        margin: 20px 0 12px 0;
    }
    
    .info-box {
        background: #051a2e;
        border: 1px solid #1a4d6d;
        padding: 12px;
        border-radius: 3px;
        margin-bottom: 12px;
    }
    
    .info-box-title {
        color: #7a8fa0;
        font-size: 9px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin: 0 0 4px 0;
    }
    
    .info-box-content {
        color: #e0e0e0;
        font-size: 12px;
        margin: 4px 0 0 0;
        font-weight: bold;
    }
    
    .info-box-small {
        color: #7a8fa0;
        font-size: 9px;
        margin: 4px 0 0 0;
    }
    
    input {
        background-color: #051a2e !important;
        border: 1px solid #1a4d6d !important;
        color: #e0e0e0 !important;
        border-radius: 2px !important;
        padding: 8px 10px !important;
        font-size: 11px !important;
        font-family: 'Courier New', monospace !important;
    }
    
    input:focus {
        border-color: #00d4ff !important;
        outline: none !important;
        box-shadow: 0 0 6px rgba(0, 212, 255, 0.1) !important;
    }
    
    button {
        background-color: #0d3f5a !important;
        color: #00d4ff !important;
        border: 1px solid #1a7a9f !important;
        border-radius: 2px !important;
        padding: 10px !important;
        font-size: 10px !important;
        font-weight: bold !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        font-family: 'Courier New', monospace !important;
    }
    
    button:hover {
        background-color: #0f5a7f !important;
        border-color: #00d4ff !important;
    }
    
    hr {
        border: none !important;
        border-top: 1px solid #1a4d6d !important;
        margin: 15px 0 !important;
    }
    
    .file-uploader-label {
        color: #7a8fa0;
        font-size: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 4px;
        display: block;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="display: flex; gap: 12px; margin-bottom: 30px; padding: 0 8px;">
        <div style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #1a5a7a, #0d2b45); border: 1px solid #1a7a9f; border-radius: 4px; color: #00d4ff; font-size: 20px;">🛰️</div>
        <div style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; background: #051a2e; border: 1px solid #1a4d6d; border-radius: 4px; color: #7a8fa0; font-size: 18px; cursor: pointer;">📋</div>
        <div style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; background: #051a2e; border: 1px solid #1a4d6d; border-radius: 4px; color: #7a8fa0; font-size: 18px; cursor: pointer;">⏱️</div>
        <div style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; background: #051a2e; border: 1px solid #1a4d6d; border-radius: 4px; color: #7a8fa0; font-size: 18px; cursor: pointer;">📊</div>
        <div style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; background: #051a2e; border: 1px solid #1a4d6d; border-radius: 4px; color: #7a8fa0; font-size: 18px; cursor: pointer;">🗂️</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #0d2b45; border: 1px solid #1a4d6d; padding: 16px; border-radius: 2px; margin-bottom: 20px;">
        <h2 style="color: #e0e0e0; margin: 0; font-size: 16px; letter-spacing: 2px;">SATELLA</h2>
        <p style="color: #7a8fa0; font-size: 9px; margin: 4px 0 0 0; letter-spacing: 1px;">GEO-INTELLIGENCE PLATFORM</p>
        <span style="background: #00a855; color: white; padding: 3px 6px; border-radius: 2px; font-size: 7px; margin-top: 8px; display: inline-block; font-weight: bold;">● LIVE</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">▶ CURRENT PROJECT</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        <p class="info-box-content">Baku Urban Expansion</p>
        <p class="info-box-small">ID: AZ-BU-2025-09</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-title">🎯 TARGET COORDINATES</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="small")
    with col1:
        st.markdown('<label class="file-uploader-label">LATITUDE</label>', unsafe_allow_html=True)
        lat_input = st.text_input("", value=str(st.session_state.lat), label_visibility="collapsed", key="lat_input")
    with col2:
        st.markdown('<label class="file-uploader-label">LONGITUDE</label>', unsafe_allow_html=True)
        lon_input = st.text_input("", value=str(st.session_state.lon), label_visibility="collapsed", key="lon_input")
    
    if st.button("🔄 Relocate Scanner", use_container_width=True):
        try:
            st.session_state.lat = float(lat_input)
            st.session_state.lon = float(lon_input)
            st.rerun()
        except:
            st.error("Invalid coordinates")
    
    st.markdown("---")
    
    st.markdown('<div class="section-title">⚙️ INGEST ENGINE</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <p class="info-box-title">📦 Baseline Imagery (T0)</p>
        <p class="info-box-small">Sentinel-2 L2A</p>
    </div>
    """, unsafe_allow_html=True)
    t0_file = st.file_uploader("", type=["png", "jpg", "jpeg"], label_visibility="collapsed", key="t0_up")
    
    st.markdown("""
    <div class="info-box">
        <p class="info-box-title">▶️ Target Imagery (T1)</p>
        <p class="info-box-small">Sentinel-2 L2A</p>
    </div>
    """, unsafe_allow_html=True)
    t1_file = st.file_uploader("", type=["png", "jpg", "jpeg"], label_visibility="collapsed", key="t1_up")
    
    if t0_file:
        st.session_state.t0 = t0_file
    if t1_file:
        st.session_state.t1 = t1_file
    
    st.markdown("---")
    
    if st.button("▶ INITIALIZE AI ANALYSIS", use_container_width=True):
        if st.session_state.t0 and st.session_state.t1:
            st.session_state.is_analysed = True
            st.balloons()
            st.rerun()
        else:
            st.error("Upload both files")
    
    st.markdown("""
    <div style="position: fixed; bottom: 20px; left: 20px; width: calc(100% - 40px);">
        <div style="display: flex; gap: 12px;">
            <div style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; background: #051a2e; border: 1px solid #1a4d6d; border-radius: 4px; color: #7a8fa0; font-size: 18px; cursor: pointer;">⚙️</div>
            <div style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; background: #051a2e; border: 1px solid #1a4d6d; border-radius: 4px; color: #7a8fa0; font-size: 18px; cursor: pointer;">👤</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

col_map, col_panel = st.columns([3.5, 1.2], gap="small")

with col_map:
    lat = st.session_state.lat
    lon = st.session_state.lon
    
    m = folium.Map(location=[lat, lon], zoom_start=18)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri"
    ).add_to(m)
    folium.Marker([lat, lon], popup="Target").add_to(m)
    
    folium_static(m, width=1050, height=700)

with col_panel:
    st.markdown("""
    <div class="info-box">
        <p class="info-box-title">🔍 DETECTION LAYER</p>
    </div>
    """, unsafe_allow_html=True)
    
    detections = "1" if st.session_state.is_analysed else "0"
    st.markdown(f"""
    <div class="info-box">
        <p class="info-box-title">Structural Detections</p>
        <p style="color: #00d4ff; font-size: 24px; font-weight: bold; margin: 6px 0 0 0;">{detections}</p>
    </div>
    """, unsafe_allow_html=True)
    
    confidence = "92.4" if st.session_state.is_analysed else "0.0"
    st.markdown(f"""
    <div class="info-box">
        <p class="info-box-title">AI Confidence</p>
        <p style="color: #00d4ff; font-size: 24px; font-weight: bold; margin: 6px 0 0 0;">{confidence}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <p class="info-box-title">📥 EXPORT PROTOCOL</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.is_analysed:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "SATELLA AI REPORT", ln=True, align='C')
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 8, f"Location: {lat}, {lon}", ln=True)
        pdf.cell(0, 8, f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
        pdf_data = pdf.output(dest='S').encode('latin-1', 'ignore')
        
        st.download_button(
            label="⬇ Download Report",
            data=pdf_data,
            file_name=f"SATELLA_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    st.markdown("""
    <div class="info-box">
        <p class="info-box-title">📷 IMAGERY FEED</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.t0:
        st.markdown('<p style="color: #00d4ff; font-size: 8px; text-align: center; margin: 6px 0 4px 0; text-transform: uppercase;">REF: 2024</p>', unsafe_allow_html=True)
        st.image(st.session_state.t0, use_container_width=True)
    
    if st.session_state.t1:
        st.markdown('<p style="color: #00d4ff; font-size: 8px; text-align: center; margin: 6px 0 4px 0; text-transform: uppercase;">TARGET: 2025</p>', unsafe_allow_html=True)
        st.image(st.session_state.t1, use_container_width=True)
