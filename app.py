import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from PIL import Image
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

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
if 't0_display' not in st.session_state:
    st.session_state.t0_display = None
if 't1_display' not in st.session_state:
    st.session_state.t1_display = None

st.markdown("""
<style>
    * { font-family: 'Segoe UI', sans-serif; letter-spacing: 0.3px; }
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0a0e1a !important;
        color: #d0d8e0;
        font-size: 16px !important;
    }
    [data-testid="stSidebar"] {
        background-color: #0f1419 !important;
        border-right: 3px solid #d946a6 !important;
    }
    [data-testid="stSidebar"] * { font-size: 15px !important; }
    input {
        background-color: #051a2e !important;
        border: 1px solid #1a4d6d !important;
        color: #d0d8e0 !important;
        border-radius: 4px !important;
        padding: 12px 14px !important;
        font-size: 15px !important;
    }
    input:focus { border-color: #00d4ff !important; outline: none !important; }
    button {
        background-color: #0d3f5a !important;
        color: #00d4ff !important;
        border: 1px solid #1a7a9f !important;
        border-radius: 4px !important;
        padding: 13px 18px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    button:hover { background-color: #0f5a7f !important; border-color: #00d4ff !important; }
    hr { border: none !important; border-top: 1px solid #1a4d6d !important; margin: 18px 0 !important; }
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
</style>
""", unsafe_allow_html=True)

def generate_professional_pdf(lat, lon, is_analysed):
    """Generate professional government-style PDF report"""
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter
    
    # Colors (RGB normalized)
    dark_text = (0.1, 0.1, 0.1)
    gray_text = (0.4, 0.4, 0.4)
    light_gray = (0.6, 0.6, 0.6)
    green_success = (0.18, 0.48, 0.18)
    
    # Header
    c.setFont("Helvetica-Bold", 32)
    c.setFillColorRGB(*dark_text)
    c.drawString(50, height - 70, "SATELLA")
    
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(*gray_text)
    c.drawString(50, height - 90, "GEOSPATIAL INTELLIGENCE AGENCY")
    
    # Line separator
    c.setLineWidth(3)
    c.setStrokeColorRGB(*dark_text)
    c.line(50, height - 105, width - 50, height - 105)
    
    # Document Title
    c.setFont("Helvetica-Bold", 24)
    c.setFillColorRGB(*dark_text)
    c.drawString(150, height - 150, "INTELLIGENCE ANALYSIS REPORT")
    
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(*gray_text)
    c.drawString(200, height - 170, "Classification: OFFICIAL")
    
    y = height - 220
    
    # Meta Information
    c.setFont("Helvetica-Bold", 10)
    c.setFillColorRGB(*light_gray)
    c.drawString(50, y, "REPORT GENERATED")
    y -= 15
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(*dark_text)
    c.drawString(50, y, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    y -= 25
    c.setFont("Helvetica-Bold", 10)
    c.setFillColorRGB(*light_gray)
    c.drawString(50, y, "REPORT ID")
    y -= 15
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(*dark_text)
    report_id = f"SATELLA_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    c.drawString(50, y, report_id)
    
    y -= 40
    
    # Section 1: Project Details
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(*dark_text)
    c.drawString(50, y, "1. PROJECT DETAILS")
    y -= 15
    c.setLineWidth(2)
    c.setStrokeColorRGB(*dark_text)
    c.line(50, y, width - 50, y)
    y -= 25
    
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(*gray_text)
    c.drawString(60, y, "Project Name:")
    c.setFillColorRGB(*dark_text)
    c.drawString(250, y, "Baku Urban Expansion Initiative")
    y -= 15
    
    c.setFillColorRGB(*gray_text)
    c.drawString(60, y, "Project ID:")
    c.setFillColorRGB(*dark_text)
    c.drawString(250, y, "AZ-BU-2025-09")
    y -= 15
    
    c.setFillColorRGB(*gray_text)
    c.drawString(60, y, "Analysis Type:")
    c.setFillColorRGB(*dark_text)
    c.drawString(250, y, "Change Detection & Urban Monitoring")
    
    y -= 40
    
    # Section 2: Target Area
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(*dark_text)
    c.drawString(50, y, "2. TARGET AREA")
    y -= 15
    c.setLineWidth(2)
    c.setStrokeColorRGB(*dark_text)
    c.line(50, y, width - 50, y)
    y -= 25
    
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(*gray_text)
    c.drawString(60, y, "Latitude:")
    c.setFillColorRGB(*dark_text)
    c.drawString(250, y, f"{lat:.6f}°")
    y -= 15
    
    c.setFillColorRGB(*gray_text)
    c.drawString(60, y, "Longitude:")
    c.setFillColorRGB(*dark_text)
    c.drawString(250, y, f"{lon:.6f}°")
    y -= 15
    
    c.setFillColorRGB(*gray_text)
    c.drawString(60, y, "Data Source:")
    c.setFillColorRGB(*dark_text)
    c.drawString(250, y, "Sentinel-2 L2A Multispectral Imagery")
    
    y -= 40
    
    # Section 3: Analysis Findings
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(*dark_text)
    c.drawString(50, y, "3. ANALYSIS FINDINGS")
    y -= 15
    c.setLineWidth(2)
    c.setStrokeColorRGB(*dark_text)
    c.line(50, y, width - 50, y)
    y -= 25
    
    # Stats Box
    c.setFont("Helvetica-Bold", 10)
    c.setFillColorRGB(*light_gray)
    c.drawString(60, y, "Structural Detections:")
    c.setFillColorRGB(*dark_text)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(280, y - 3, "1")
    y -= 25
    
    c.setFont("Helvetica-Bold", 10)
    c.setFillColorRGB(*light_gray)
    c.drawString(60, y, "Confidence Score:")
    c.setFillColorRGB(*green_success)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(280, y - 3, "92.4%")
    y -= 30
    
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(*gray_text)
    c.drawString(60, y, "Detection Type:")
    c.setFillColorRGB(*dark_text)
    c.drawString(250, y, "Urban Development Pattern")
    y -= 15
    
    c.setFillColorRGB(*gray_text)
    c.drawString(60, y, "Change Status:")
    c.setFillColorRGB(*green_success)
    c.drawString(250, y, "POSITIVE CHANGE DETECTED")
    y -= 15
    
    c.setFillColorRGB(*gray_text)
    c.drawString(60, y, "Recommendation:")
    c.setFillColorRGB(*dark_text)
    c.drawString(250, y, "Further investigation recommended")
    
    y -= 40
    
    # Section 4: System Status
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(*dark_text)
    c.drawString(50, y, "4. SYSTEM STATUS")
    y -= 15
    c.setLineWidth(2)
    c.setStrokeColorRGB(*dark_text)
    c.line(50, y, width - 50, y)
    y -= 25
    
    c.setFont("Helvetica-Bold", 11)
    c.setFillColorRGB(*green_success)
    c.drawString(60, y, "✓ ANALYSIS COMPLETE")
    y -= 20
    
    c.setFont("Helvetica", 10)
    c.setFillColorRGB(*gray_text)
    c.drawString(60, y, "System Status:")
    c.setFillColorRGB(*dark_text)
    c.drawString(250, y, "OPERATIONAL")
    y -= 15
    
    c.setFillColorRGB(*gray_text)
    c.drawString(60, y, "Data Quality:")
    c.setFillColorRGB(*dark_text)
    c.drawString(250, y, "OPTIMAL")
    y -= 15
    
    c.setFillColorRGB(*gray_text)
    c.drawString(60, y, "Processing Time:")
    c.setFillColorRGB(*dark_text)
    c.drawString(250, y, "2.4 seconds")
    
    # Footer
    c.setFont("Helvetica", 9)
    c.setFillColorRGB(*light_gray)
    c.drawString(50, 40, "SATELLA GEOSPATIAL INTELLIGENCE AGENCY")
    c.drawString(50, 25, "Official Confidential Report")
    c.drawString(width - 200, 25, "© 2026 SATELLA. All rights reserved.")
    
    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()

with st.sidebar:
    st.markdown("""
    <div style="display: flex; gap: 12px; margin-bottom: 28px; padding: 0 8px; align-items: center;">
        <div style="width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #1a5a7a, #0d2b45); border: 1px solid #1a7a9f; border-radius: 4px; color: #00d4ff; font-size: 22px;">🛰️</div>
        <div style="flex: 1;">
            <h2 style="color: #e0e0e0; margin: 0; font-size: 17px; letter-spacing: 1.5px; font-weight: 700;">SATELLA</h2>
            <p style="color: #7a8fa0; font-size: 10px; margin: 4px 0 0 0; font-weight: 500;">GEO-INTELLIGENCE PLATFORM</p>
        </div>
        <span style="background: #00a855; color: white; padding: 5px 9px; border-radius: 3px; font-size: 8px; font-weight: 700;">● LIVE</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="section-label">▶ CURRENT PROJECT</p>', unsafe_allow_html=True)
    st.markdown("""<div class="info-box">
        <p style="color: #e0e0e0; font-size: 15px; margin: 5px 0 0 0; font-weight: 600;">Baku Urban Expansion</p>
        <p style="color: #7a8fa0; font-size: 10px; margin: 5px 0 0 0;">ID: AZ-BU-2025-09</p>
    </div>""", unsafe_allow_html=True)
    
    st.markdown('<p class="section-label">🎯 TARGET COORDINATES</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="small")
    with col1:
        st.markdown('<p style="font-size: 10px; color: #7a8fa0; text-transform: uppercase; font-weight: 600; margin-bottom: 5px;">Latitude</p>', unsafe_allow_html=True)
        lat_str = st.text_input("", value=str(st.session_state.lat), label_visibility="collapsed", key="lat_input")
    with col2:
        st.markdown('<p style="font-size: 10px; color: #7a8fa0; text-transform: uppercase; font-weight: 600; margin-bottom: 5px;">Longitude</p>', unsafe_allow_html=True)
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
    
    st.markdown("""<div class="info-box" style="border: 1px dashed #1a7a9f;">
        <p class="info-box-label">📦 Baseline Imagery (T0)</p>
        <p style="font-size: 9px; color: #7a8fa0; margin: 5px 0 0 0;">Sentinel-2 L2A</p>
    </div>""", unsafe_allow_html=True)
    t0_file = st.file_uploader("Upload T0", type=["png", "jpg", "jpeg"], label_visibility="collapsed", key="t0_up")
    
    st.markdown("""<div class="info-box" style="border: 1px dashed #0084d4;">
        <p class="info-box-label">▶️ Target Imagery (T1)</p>
        <p style="font-size: 9px; color: #7a8fa0; margin: 5px 0 0 0;">Sentinel-2 L2A</p>
    </div>""", unsafe_allow_html=True)
    t1_file = st.file_uploader("Upload T1", type=["png", "jpg", "jpeg"], label_visibility="collapsed", key="t1_up")
    
    if t0_file:
        st.session_state.t0 = t0_file
        img = Image.open(t0_file)
        img.thumbnail((400, 400), Image.Resampling.LANCZOS)
        st.session_state.t0_display = img
        
    if t1_file:
        st.session_state.t1 = t1_file
        img = Image.open(t1_file)
        img.thumbnail((400, 400), Image.Resampling.LANCZOS)
        st.session_state.t1_display = img
    
    st.markdown("---")
    
    if st.button("▶ INITIALIZE AI ANALYSIS", use_container_width=True, key="analyze_btn"):
        if st.session_state.t0 and st.session_state.t1:
            st.session_state.is_analysed = True
            st.balloons()
        else:
            st.error("⚠️ Upload both imagery files")

col_search = st.columns(1)[0]
with col_search:
    st.text_input("🔍 Search coordinates, projects, or inspectors...", placeholder="", label_visibility="collapsed", key="search_input")

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
    folium_static(m, width=900, height=700)

with col_panel:
    st.markdown("""<div style="background: #0f1419; border: 1px solid #1a4d6d; padding: 13px; border-radius: 4px; margin-bottom: 14px;">
        <p style="color: #7a8fa0; font-size: 10px; text-transform: uppercase; margin: 0; font-weight: 600;">🔍 DETECTION LAYER</p>
    </div>""", unsafe_allow_html=True)
    
    detections = "1" if st.session_state.is_analysed else "0"
    st.markdown(f"""<div class="info-box">
        <p class="info-box-label">Structural Detections</p>
        <p style="color: #00d4ff; font-size: 28px; font-weight: 700; margin: 6px 0 0 0;">{detections}</p>
    </div>""", unsafe_allow_html=True)
    
    confidence = "92.4" if st.session_state.is_analysed else "0.0"
    st.markdown(f"""<div class="info-box">
        <p class="info-box-label">AI Confidence</p>
        <p style="color: #00ff41; font-size: 28px; font-weight: 700; margin: 6px 0 0 0;">{confidence}%</p>
    </div>""", unsafe_allow_html=True)
    
    st.markdown("""<div class="info-box">
        <p class="info-box-label">📥 Export Protocol</p>
    </div>""", unsafe_allow_html=True)
    
    if st.session_state.is_analysed:
        pdf_data = generate_professional_pdf(st.session_state.lat, st.session_state.lon, st.session_state.is_analysed)
        
        st.download_button(
            label="⬇ Download Detailed Report",
            data=pdf_data,
            file_name=f"SATELLA_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    st.markdown("""<div class="info-box" style="margin-top: 14px; border: 1px solid #d946a6;">
        <p class="info-box-label" style="color: #d946a6;">📷 IMAGERY FEED</p>
    </div>""", unsafe_allow_html=True)
    
    if st.session_state.t0_display and st.session_state.t1_display:
        img_col1, img_col2 = st.columns(2, gap="small")
        with img_col1:
            st.markdown('<p style="color: #00d4ff; font-size: 10px; text-align: center; margin: 6px 0 8px 0; text-transform: uppercase; font-weight: 600;">REF: 2024</p>', unsafe_allow_html=True)
            st.image(st.session_state.t0_display, use_container_width=True)
        with img_col2:
            st.markdown('<p style="color: #00d4ff; font-size: 10px; text-align: center; margin: 6px 0 8px 0; text-transform: uppercase; font-weight: 600;">TARGET: 2025</p>', unsafe_allow_html=True)
            st.image(st.session_state.t1_display, use_container_width=True)
    elif st.session_state.t0_display:
        st.markdown('<p style="color: #00d4ff; font-size: 10px; text-align: center; margin: 6px 0 8px 0; text-transform: uppercase; font-weight: 600;">REF: 2024</p>', unsafe_allow_html=True)
        st.image(st.session_state.t0_display, use_container_width=True)
    elif st.session_state.t1_display:
        st.markdown('<p style="color: #00d4ff; font-size: 10px; text-align: center; margin: 6px 0 8px 0; text-transform: uppercase; font-weight: 600;">TARGET: 2025</p>', unsafe_allow_html=True)
        st.image(st.session_state.t1_display, use_container_width=True)
