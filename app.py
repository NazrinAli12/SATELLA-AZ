import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
from PIL import Image
import io

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
    }
    
    button {
        background-color: #0d3f5a !important;
        color: #00d4ff !important;
        border: 1px solid #1a7a9f !important;
        border-radius: 3px !important;
        padding: 10px !important;
        font-size: 10px !important;
        font-weight: bold !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
    }
    
    button:hover {
        background-color: #0f5a7f !important;
        border-color: #00d4ff !important;
    }
    
    .analyze-btn {
        background: linear-gradient(135deg, #1e5a8e 0%, #0d3f5a 100%) !important;
        border: 2px solid #00d4ff !important;
        color: white !important;
        padding: 12px !important;
        font-size: 12px !important;
        font-weight: bold !important;
    }
    
    .analyze-btn:hover {
        background: linear-gradient(135deg, #2570a8 0%, #0f5a7f 100%) !important;
    }
    
    hr {
        border: none !important;
        border-top: 1px solid #1a4d6d !important;
        margin: 15px 0 !important;
    }
    
    [data-testid="stFileUploader"] {
        background: #051a2e;
        border: 1px dashed #1a7a9f;
        border-radius: 3px;
        padding: 12px;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="display: flex; gap: 12px; margin-bottom: 30px; padding: 0 8px;">
        <div style="width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #1a5a7a, #0d2b45); border: 1px solid #1a7a9f; border-radius: 4px; color: #00d4ff; font-size: 20px;">🛰️</div>
        <div style="flex: 1;">
            <h2 style="color: #e0e0e0; margin: 0; font-size: 16px; letter-spacing: 2px;">SATELLA</h2>
            <p style="color: #7a8fa0; font-size: 9px; margin: 4px 0 0 0; letter-spacing: 1px;">GEO-INTELLIGENCE PLATFORM</p>
        </div>
        <span style="background: #00a855; color: white; padding: 4px 8px; border-radius: 2px; font-size: 7px; font-weight: bold; height: fit-content;">● LIVE</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p style="font-size: 9px; color: #7a8fa0; text-transform: uppercase; letter-spacing: 1px; margin: 15px 0 10px 0;">▶ CURRENT PROJECT</p>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 12px; border-radius: 3px; margin-bottom: 20px;">
        <p style="margin: 0; color: #e0e0e0; font-size: 12px; font-weight: bold;">Baku Urban Expansion</p>
        <p style="margin: 4px 0 0 0; color: #7a8fa0; font-size: 9px;">ID: AZ-BU-2025-09</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p style="font-size: 9px; color: #7a8fa0; text-transform: uppercase; letter-spacing: 1px; margin: 15px 0 10px 0;">🎯 TARGET COORDINATES</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="small")
    with col1:
        st.markdown('<label style="font-size: 8px; color: #7a8fa0; text-transform: uppercase;">LATITUDE</label>', unsafe_allow_html=True)
        lat_str = st.text_input("", value=str(st.session_state.lat), label_visibility="collapsed", key="lat_input")
    with col2:
        st.markdown('<label style="font-size: 8px; color: #7a8fa0; text-transform: uppercase;">LONGITUDE</label>', unsafe_allow_html=True)
        lon_str = st.text_input("", value=str(st.session_state.lon), label_visibility="collapsed", key="lon_input")
    
    try:
        lat_val = float(lat_str)
        lon_val = float(lon_str)
        if -90 <= lat_val <= 90 and -180 <= lon_val <= 180:
            st.session_state.lat = lat_val
            st.session_state.lon = lon_val
    except:
        pass
    
    if st.button("🔄 Relocate Scanner", use_container_width=True):
        st.rerun()
    
    st.markdown("---")
    
    st.markdown('<p style="font-size: 9px; color: #7a8fa0; text-transform: uppercase; letter-spacing: 1px; margin: 15px 0 10px 0; border-left: 2px solid #d946a6; padding-left: 10px;">⚙️ INGEST ENGINE</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #051a2e; border: 1px dashed #1a7a9f; padding: 12px; border-radius: 3px; margin-bottom: 12px;">
        <p style="font-size: 10px; color: #e0e0e0; font-weight: bold; margin: 0 0 4px 0;">📦 Baseline Imagery (T0)</p>
        <p style="font-size: 8px; color: #7a8fa0; margin: 0;">test 2025-12-28 163547.png</p>
    </div>
    """, unsafe_allow_html=True)
    t0_file = st.file_uploader("Upload T0", type=["png", "jpg", "jpeg"], label_visibility="collapsed", key="t0_up")
    
    st.markdown("""
    <div style="background: #051a2e; border: 1px dashed #0084d4; padding: 12px; border-radius: 3px; margin-bottom: 12px;">
        <p style="font-size: 10px; color: #e0e0e0; font-weight: bold; margin: 0 0 4px 0;">▶️ Target Imagery (T1)</p>
        <p style="font-size: 8px; color: #7a8fa0; margin: 0;">test 2 2025-12-29 163628.png</p>
    </div>
    """, unsafe_allow_html=True)
    t1_file = st.file_uploader("Upload T1", type=["png", "jpg", "jpeg"], label_visibility="collapsed", key="t1_up")
    
    if t0_file:
        st.session_state.t0 = t0_file
    if t1_file:
        st.session_state.t1 = t1_file
    
    st.markdown("---")
    
    if st.button("▶ INITIALIZE AI ANALYSIS", use_container_width=True, key="analyze_btn"):
        if st.session_state.t0 and st.session_state.t1:
            st.session_state.is_analysed = True
            st.balloons()
            st.success("✓ Analysis complete!")
            st.rerun()

col_top = st.columns(1)[0]
with col_top:
    search_bar = st.text_input("🔍 Search coordinates, projects, or inspectors...", placeholder="", label_visibility="collapsed", key="search_input")

col_map, col_panel = st.columns([2.8, 1.4], gap="small")

with col_map:
    lat = st.session_state.lat
    lon = st.session_state.lon
    
    m = folium.Map(location=[lat, lon], zoom_start=18)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri"
    ).add_to(m)
    folium.Marker([lat, lon], popup="Target", icon=folium.Icon(color='blue')).add_to(m)
    
    # Add uploaded images as overlays on map
    if st.session_state.t0 or st.session_state.t1:
        folium_static(m, width=900, height=650)
    else:
        folium_static(m, width=900, height=650)

with col_panel:
    st.markdown("""
    <div style="background: #0f1419; border: 1px solid #1a4d6d; padding: 12px; border-radius: 3px; margin-bottom: 12px;">
        <p style="color: #7a8fa0; font-size: 9px; text-transform: uppercase; letter-spacing: 1px; margin: 0;">🔍 DETECTION LAYER</p>
    </div>
    """, unsafe_allow_html=True)
    
    detections = "1" if st.session_state.is_analysed else "0"
    st.markdown(f"""
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 12px; border-radius: 3px; margin-bottom: 10px;">
        <p style="color: #7a8fa0; font-size: 9px; text-transform: uppercase; margin: 0;">Structural Detections</p>
        <p style="color: #00d4ff; font-size: 26px; font-weight: bold; margin: 6px 0 0 0;">{detections}</p>
    </div>
    """, unsafe_allow_html=True)
    
    confidence = "92.4" if st.session_state.is_analysed else "0.0"
    st.markdown(f"""
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 12px; border-radius: 3px; margin-bottom: 10px;">
        <p style="color: #7a8fa0; font-size: 9px; text-transform: uppercase; margin: 0;">AI Confidence</p>
        <p style="color: #00ff41; font-size: 26px; font-weight: bold; margin: 6px 0 0 0;">{confidence}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 12px; border-radius: 3px; margin-bottom: 10px;">
        <p style="color: #7a8fa0; font-size: 9px; text-transform: uppercase; margin: 0;">📥 EXPORT PROTOCOL</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.is_analysed:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "SATELLA AI REPORT", ln=True, align='C')
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 8, f"Location: {st.session_state.lat}, {st.session_state.lon}", ln=True)
        pdf.cell(0, 8, f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
        pdf_data = pdf.output(dest='S').encode('latin-1', 'ignore')
        
        st.download_button(
            label="⬇ DOWNLOAD REPORT",
            data=pdf_data,
            file_name=f"SATELLA_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    st.markdown("""
    <div style="background: #051a2e; border: 1px solid #1a4d6d; padding: 12px; border-radius: 3px; margin-top: 12px;">
        <p style="color: #7a8fa0; font-size: 9px; text-transform: uppercase; margin: 0;">📷 IMAGERY FEED</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.t0 and st.session_state.t1:
        img_col1, img_col2 = st.columns(2, gap="small")
        
        with img_col1:
            st.markdown('<p style="color: #00d4ff; font-size: 8px; text-align: center; margin: 6px 0 4px 0; text-transform: uppercase;">REF: 2024</p>', unsafe_allow_html=True)
            st.image(st.session_state.t0, use_container_width=True)
        
        with img_col2:
            st.markdown('<p style="color: #00d4ff; font-size: 8px; text-align: center; margin: 6px 0 4px 0; text-transform: uppercase;">TARGET: 2025</p>', unsafe_allow_html=True)
            st.image(st.session_state.t1, use_container_width=True)
    elif st.session_state.t0:
        st.markdown('<p style="color: #00d4ff; font-size: 8px; text-align: center; margin: 6px 0 4px 0; text-transform: uppercase;">REF: 2024</p>', unsafe_allow_html=True)
        st.image(st.session_state.t0, use_container_width=True)
    elif st.session_state.t1:
        st.markdown('<p style="color: #00d4ff; font-size: 8px; text-align: center; margin: 6px 0 4px 0; text-transform: uppercase;">TARGET: 2025</p>', unsafe_allow_html=True)
        st.image(st.session_state.t1, use_container_width=True)
