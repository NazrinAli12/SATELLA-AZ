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
        color: #e0e0e0;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0f1419 !important;
        border-right: 3px solid #d946a6 !important;
    }
    
    input {
        background-color: #051a2e !important;
        border: 1px solid #1a4d6d !important;
        color: #e0e0e0 !important;
        border-radius: 2px !important;
        padding: 8px 10px !important;
        font-size: 11px !important;
    }
    
    input:focus {
        border-color: #00d4ff !important;
        outline: none !important;
    }
    
    button {
        background-color: #0d3f5a !important;
        color: #00d4ff !important;
        border: 1px solid #1a7a9f !important;
        border-radius: 2px !important;
        padding: 8px 14px !important;
        font-size: 10px !important;
        font-weight: bold !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
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
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="background: #0d2b45; border: 1px solid #1a4d6d; padding: 16px; border-radius: 2px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 24px;">🛰️</span>
            <div>
                <h2 style="color: #e0e0e0; margin: 0; font-size: 16px; letter-spacing: 2px;">SATELLA</h2>
                <p style="color: #7a8fa0; font-size: 9px; margin: 2px 0 0 0; letter-spacing: 1px;">GEO-INTELLIGENCE PLATFORM</p>
            </div>
            <span style="background: #00a855; color: white; padding: 3px 6px; border-radius: 2px; font-size: 7px; margin-left: auto; font-weight: bold;">● LIVE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p style="font-size: 8px; color: #7a8fa0; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">▶ CURRENT PROJECT</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 10px; border-radius: 2px; margin-bottom: 20px;">
        <p style="margin: 0; color: #e0e0e0; font-size: 11px; font-weight: bold;">Baku Urban Expansion</p>
        <p style="margin: 4px 0 0 0; color: #7a8fa0; font-size: 8px;">ID: AZ-BU-2025-09</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p style="font-size: 8px; color: #7a8fa0; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px;">🎯 TARGET COORDINATES</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<label style="font-size: 8px; color: #7a8fa0; text-transform: uppercase;">LATITUDE</label>', unsafe_allow_html=True)
        lat_input = st.text_input("", value=str(st.session_state.lat), label_visibility="collapsed", key="lat_input")
    with col2:
        st.markdown('<label style="font-size: 8px; color: #7a8fa0; text-transform: uppercase;">LONGITUDE</label>', unsafe_allow_html=True)
        lon_input = st.text_input("", value=str(st.session_state.lon), label_visibility="collapsed", key="lon_input")
    
    if st.button("🔄 Relocate Scanner", use_container_width=True):
        try:
            st.session_state.lat = float(lat_input)
            st.session_state.lon = float(lon_input)
            st.rerun()
        except:
            st.error("Invalid coordinates")
    
    st.markdown("---")
    
    st.markdown('<p style="font-size: 8px; color: #7a8fa0; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">⚙️ INGEST ENGINE</p>', unsafe_allow_html=True)
    
    st.markdown('<p style="font-size: 9px; color: #e0e0e0; font-weight: bold; margin-bottom: 2px;">📦 Baseline Imagery (T0)</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 8px; color: #7a8fa0; margin-bottom: 6px;">Sentinel-2 L2A</p>', unsafe_allow_html=True)
    t0_file = st.file_uploader("", type=["png", "jpg", "jpeg"], label_visibility="collapsed", key="t0_up")
    
    st.markdown('<p style="font-size: 9px; color: #e0e0e0; font-weight: bold; margin: 10px 0 2px 0;">▶️ Target Imagery (T1)</p>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 8px; color: #7a8fa0; margin-bottom: 6px;">Sentinel-2 L2A</p>', unsafe_allow_html=True)
    t1_file = st.file_uploader("", type=["png", "jpg", "jpeg"], label_visibility="collapsed", key="t1_up")
    
    if t0_file:
        st.session_state.t0 = t0_file
    if t1_file:
        st.session_state.t1 = t1_file
    
    st.markdown("---")
    
    if st.button("▶ Initialize AI Analysis", use_container_width=True):
        if st.session_state.t0 and st.session_state.t1:
            st.session_state.is_analysed = True
            st.balloons()
            st.rerun()
        else:
            st.error("Upload both files")

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
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 10px; border-radius: 2px; margin-bottom: 10px;">
        <p style="color: #7a8fa0; font-size: 8px; text-transform: uppercase; letter-spacing: 1px; margin: 0;">🔍 DETECTION LAYER</p>
    </div>
    """, unsafe_allow_html=True)
    
    detections = "1" if st.session_state.is_analysed else "0"
    st.markdown(f"""
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 10px; border-radius: 2px; margin-bottom: 10px;">
        <p style="color: #7a8fa0; font-size: 8px; text-transform: uppercase; margin: 0;">Structural Detections</p>
        <p style="color: #00d4ff; font-size: 24px; font-weight: bold; margin: 6px 0 0 0;">{detections}</p>
    </div>
    """, unsafe_allow_html=True)
    
    confidence = "92.4" if st.session_state.is_analysed else "0.0"
    st.markdown(f"""
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 10px; border-radius: 2px; margin-bottom: 10px;">
        <p style="color: #7a8fa0; font-size: 8px; text-transform: uppercase; margin: 0;">AI Confidence</p>
        <p style="color: #00d4ff; font-size: 24px; font-weight: bold; margin: 6px 0 0 0;">{confidence}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 10px; border-radius: 2px; margin-bottom: 10px;">
        <p style="color: #7a8fa0; font-size: 8px; text-transform: uppercase; margin: 0;">📥 EXPORT PROTOCOL</p>
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
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 10px; border-radius: 2px; margin-top: 10px;">
        <p style="color: #7a8fa0; font-size: 8px; text-transform: uppercase; margin: 0;">📷 IMAGERY FEED</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.t0:
        st.markdown('<p style="color: #00d4ff; font-size: 8px; text-align: center; margin: 6px 0 4px 0; text-transform: uppercase;">REF: 2024</p>', unsafe_allow_html=True)
        st.image(st.session_state.t0, use_container_width=True)
    
    if st.session_state.t1:
        st.markdown('<p style="color: #00d4ff; font-size: 8px; text-align: center; margin: 6px 0 4px 0; text-transform: uppercase;">TARGET: 2025</p>', unsafe_allow_html=True)
        st.image(st.session_state.t1, use_container_width=True)
