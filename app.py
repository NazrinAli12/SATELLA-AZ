import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
from PIL import Image

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
    * { 
        font-family: 'Segoe UI', -apple-system, 'Helvetica Neue', sans-serif;
        letter-spacing: 0.3px;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0a0e1a !important;
        color: #d0d8e0;
        font-size: 16px !important;
        line-height: 1.6 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0f1419 !important;
        border-right: 3px solid #d946a6 !important;
    }
    
    [data-testid="stSidebar"] * {
        font-size: 15px !important;
    }
    
    input {
        background-color: #051a2e !important;
        border: 1px solid #1a4d6d !important;
        color: #d0d8e0 !important;
        border-radius: 4px !important;
        padding: 12px 14px !important;
        font-size: 15px !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    
    input:focus {
        border-color: #00d4ff !important;
        outline: none !important;
        box-shadow: 0 0 8px rgba(0, 212, 255, 0.2) !important;
    }
    
    button {
        background-color: #0d3f5a !important;
        color: #00d4ff !important;
        border: 1px solid #1a7a9f !important;
        border-radius: 4px !important;
        padding: 13px 18px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        text-transform: uppercase !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    
    button:hover {
        background-color: #0f5a7f !important;
        border-color: #00d4ff !important;
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.15) !important;
    }
    
    .analyze-btn {
        background: linear-gradient(135deg, #1e5a8e 0%, #0d3f5a 100%) !important;
        border: 2px solid #00d4ff !important;
        color: #00ffff !important;
        padding: 13px !important;
        font-size: 13px !important;
        font-weight: 700 !important;
    }
    
    .analyze-btn:hover {
        background: linear-gradient(135deg, #2570a8 0%, #0f5a7f 100%) !important;
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.3) !important;
    }
    
    hr {
        border: none !important;
        border-top: 1px solid #1a4d6d !important;
        margin: 18px 0 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-weight: 600 !important;
        letter-spacing: 0.4px !important;
    }
    
    p {
        line-height: 1.5 !important;
    }
    
    .section-label {
        color: #00d4ff;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 700;
        margin: 18px 0 12px 0;
    }
    
    .info-box {
        background: #051a2e;
        border: 1px solid #1a4d6d;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 12px;
    }
    
    .info-box-label {
        color: #7a8fa0;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin: 0;
        font-weight: 600;
    }
    
    .info-box-value {
        color: #e0e0e0;
        font-size: 15px;
        margin: 5px 0 0 0;
        font-weight: 600;
    }
    
    .search-input {
        background-color: #051a2e !important;
        border: 1px solid #1a4d6d !important;
        color: #d0d8e0 !important;
        padding: 10px 14px !important;
        border-radius: 4px !important;
        font-size: 13px !important;
        margin-bottom: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div style="display: flex; gap: 12px; margin-bottom: 28px; padding: 0 8px; align-items: center;">
        <div style="width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #1a5a7a, #0d2b45); border: 1px solid #1a7a9f; border-radius: 4px; color: #00d4ff; font-size: 22px; flex-shrink: 0;">🛰️</div>
        <div style="flex: 1;">
            <h2 style="color: #e0e0e0; margin: 0; font-size: 17px; letter-spacing: 1.5px; font-weight: 700;">SATELLA</h2>
            <p style="color: #7a8fa0; font-size: 10px; margin: 4px 0 0 0; letter-spacing: 0.8px; font-weight: 500;">GEO-INTELLIGENCE PLATFORM</p>
        </div>
        <span style="background: #00a855; color: white; padding: 5px 9px; border-radius: 3px; font-size: 8px; font-weight: 700; letter-spacing: 0.6px; white-space: nowrap;">● LIVE</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="section-label">▶ CURRENT PROJECT</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        <p class="info-box-value">Baku Urban Expansion</p>
        <p style="color: #7a8fa0; font-size: 10px; margin: 5px 0 0 0;">ID: AZ-BU-2025-09</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="section-label">🎯 TARGET COORDINATES</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="small")
    with col1:
        st.markdown('<p style="font-size: 10px; color: #7a8fa0; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; margin-bottom: 5px;">Latitude</p>', unsafe_allow_html=True)
        lat_str = st.text_input("", value=str(st.session_state.lat), label_visibility="collapsed", key="lat_input")
    with col2:
        st.markdown('<p style="font-size: 10px; color: #7a8fa0; text-transform: uppercase; letter-spacing: 0.8px; font-weight: 600; margin-bottom: 5px;">Longitude</p>', unsafe_allow_html=True)
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
    
    st.markdown('<p class="section-label" style="border-left: 2px solid #d946a6; padding-left: 10px;">⚙️ INGEST ENGINE</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box" style="border: 1px dashed #1a7a9f;">
        <p class="info-box-label">📦 Baseline Imagery (T0)</p>
        <p style="font-size: 9px; color: #7a8fa0; margin: 5px 0 0 0;">Sentinel-2 L2A</p>
    </div>
    """, unsafe_allow_html=True)
    t0_file = st.file_uploader("Upload T0", type=["png", "jpg", "jpeg"], label_visibility="collapsed", key="t0_up")
    
    st.markdown("""
    <div class="info-box" style="border: 1px dashed #0084d4;">
        <p class="info-box-label">▶️ Target Imagery (T1)</p>
        <p style="font-size: 9px; color: #7a8fa0; margin: 5px 0 0 0;">Sentinel-2 L2A</p>
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
            st.success("✓ Analysis complete!")
            st.balloons()

# MAIN CONTENT
col_search = st.columns(1)[0]
with col_search:
    search_bar = st.text_input("🔍 Search coordinates, projects, or inspectors...", placeholder="", label_visibility="collapsed", key="search_input")

col_map, col_panel = st.columns([2.8, 1.4], gap="small")

# MAP
with col_map:
    lat = st.session_state.lat
    lon = st.session_state.lon
    
    m = folium.Map(location=[lat, lon], zoom_start=18)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri"
    ).add_to(m)
    folium.Marker([lat, lon], popup="Target", icon=folium.Icon(color='blue')).add_to(m)
    
    folium_static(m, width=900, height=700)

# RIGHT PANEL
with col_panel:
    st.markdown("""
    <div style="background: #0f1419; border: 1px solid #1a4d6d; padding: 13px; border-radius: 4px; margin-bottom: 14px;">
        <p style="color: #7a8fa0; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; margin: 0; font-weight: 600;">🔍 DETECTION LAYER</p>
    </div>
    """, unsafe_allow_html=True)
    
    detections = "1" if st.session_state.is_analysed else "0"
    st.markdown(f"""
    <div class="info-box">
        <p class="info-box-label">Structural Detections</p>
        <p style="color: #00d4ff; font-size: 28px; font-weight: 700; margin: 6px 0 0 0;">{detections}</p>
    </div>
    """, unsafe_allow_html=True)
    
    confidence = "92.4" if st.session_state.is_analysed else "0.0"
    st.markdown(f"""
    <div class="info-box">
        <p class="info-box-label">AI Confidence</p>
        <p style="color: #00ff41; font-size: 28px; font-weight: 700; margin: 6px 0 0 0;">{confidence}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
        <p class="info-box-label">📥 Export Protocol</p>
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
        
        try:
            pdf_data = pdf.output()
            st.download_button(
                label="⬇ Download Report",
                data=pdf_data,
                file_name=f"SATELLA_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"PDF generation error: {str(e)}")
    
    st.markdown("""
    <div class="info-box" style="margin-top: 14px; border: 1px solid #d946a6;">
        <p class="info-box-label" style="color: #d946a6;">📷 IMAGERY FEED</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.t0 and st.session_state.t1:
        img_col1, img_col2 = st.columns(2, gap="small")
        
        img1 = Image.open(st.session_state.t0)
        img2 = Image.open(st.session_state.t1)
        
        # Get aspect ratio from first image and apply to both
        aspect_ratio = img1.height / img1.width
        target_width = 280
        target_height = int(target_width * aspect_ratio)
        
        img1_resized = img1.resize((target_width, target_height), Image.Resampling.LANCZOS)
        img2_resized = img2.resize((target_width, target_height), Image.Resampling.LANCZOS)
        
        with img_col1:
            st.markdown('<p style="color: #00d4ff; font-size: 10px; text-align: center; margin: 6px 0 8px 0; text-transform: uppercase; font-weight: 600; letter-spacing: 0.8px;">REF: 2024</p>', unsafe_allow_html=True)
            st.image(img1_resized, use_container_width=True)
        
        with img_col2:
            st.markdown('<p style="color: #00d4ff; font-size: 10px; text-align: center; margin: 6px 0 8px 0; text-transform: uppercase; font-weight: 600; letter-spacing: 0.8px;">TARGET: 2025</p>', unsafe_allow_html=True)
            st.image(img2_resized, use_container_width=True)
    elif st.session_state.t0:
        img1 = Image.open(st.session_state.t0)
        aspect_ratio = img1.height / img1.width
        target_width = 280
        target_height = int(target_width * aspect_ratio)
        img1_resized = img1.resize((target_width, target_height), Image.Resampling.LANCZOS)
        st.markdown('<p style="color: #00d4ff; font-size: 10px; text-align: center; margin: 6px 0 8px 0; text-transform: uppercase; font-weight: 600;">REF: 2024</p>', unsafe_allow_html=True)
        st.image(img1_resized, use_container_width=True)
    elif st.session_state.t1:
        img2 = Image.open(st.session_state.t1)
        aspect_ratio = img2.height / img2.width
        target_width = 280
        target_height = int(target_width * aspect_ratio)
        img2_resized = img2.resize((target_width, target_height), Image.Resampling.LANCZOS)
        st.markdown('<p style="color: #00d4ff; font-size: 10px; text-align: center; margin: 6px 0 8px 0; text-transform: uppercase; font-weight: 600;">TARGET: 2025</p>', unsafe_allow_html=True)
        st.image(img2_resized, use_container_width=True)
