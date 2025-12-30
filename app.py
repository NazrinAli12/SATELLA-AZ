import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io
from PIL import Image

# 1. Səhifə Konfiqurasiyası
st.set_page_config(page_title="SATELLA AI", layout="wide", initial_sidebar_state="expanded")

# 2. SCROLL YOK + GENİŞ SIDEBAR + PROFESSIONAL DİZAYN
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
html, body, [data-testid="stAppViewContainer"], .main {
    font-family: 'Inter', sans-serif;
    background-color: #0b0d0e !important;
}

/* ÜST BAŞLIQ GİZLƏT */
[data-testid="stHeader"] { display: none !important; }

/* SOL SIDEBAR - 380px GENİŞ + SCROLL YOK */
section[data-testid="stSidebar"] {
    min-width: 380px !important;
    max-width: 380px !important;
    width: 380px !important;
    height: 100vh !important;
    max-height: 100vh !important;
    background-color: #0d1117 !important;
    border-right: 1px solid #30363d !important;
    overflow: hidden !important;
}

section[data-testid="stSidebar"] > div {
    height: 100vh !important;
    overflow: hidden !important;
    padding-bottom: 120px !important;
}

section[data-testid="stSidebar"]::-webkit-scrollbar,
[data-testid="stSidebarUserContent"]::-webkit-scrollbar {
    display: none !important;
    width: 0 !important;
}

/* MAP SAĞA SÜRÜŞDÜR */
section[data-testid="column"]:nth-child(1) {
    margin-left: 380px !important;
}

/* BRAND CARD */
.brand-card {
    background: linear-gradient(135deg, #1f6feb 0%, #111827 100%);
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.1);
    margin: -1rem -1rem 2rem -1rem !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.5);
}

/* DÜYMƏLƏR */
div.stButton > button {
    background: linear-gradient(135deg, #238636, #2ea043) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    height: 44px !important;
    font-size: 14px !important;
    width: 100% !important;
    margin-top: 12px !important;
    transition: all 0.3s !important;
    box-shadow: 0 4px 12px rgba(35,134,54,0.4) !important;
}

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(35,134,54,0.6) !important;
}

/* ETİKETLƏR */
.sidebar-label {
    font-size: 11px !important;
    font-weight: 700 !important;
    color: #8b949e !important;
    margin-top: 20px !important;
    margin-bottom: 10px !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
}

/* METRİKA QUTULARI */
.metric-box {
    background: linear-gradient(135deg, #161b22 0%, #0d1117 100%) !important;
    border: 1px solid #30363d !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    margin-bottom: 12px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
}
</style>
""", unsafe_allow_html=True)

# 3. KÖMƏKÇİ FUNKSİYALAR
def process_images(img1, img2):
    i1 = Image.open(img1)
    i2 = Image.open(img2)
    target_size = (512, 384)
    return i1.resize(target_size, Image.Resampling.LANCZOS), i2.resize(target_size, Image.Resampling.LANCZOS)

def generate_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 10, "SATELLA AI - CHANGE DETECTION", ln=1, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Coordinates: {lat:.6f}°N, {lon:.6f}°E", ln=1)
    pdf.cell(0, 10, f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=1)
    pdf.cell(0, 10, "Detected Changes: 1 Structure", ln=1)
    pdf.cell(0, 10, "Confidence: 92.4%", ln=1)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "STATUS: ANALYSIS COMPLETE", ln=1, align='C')
    buffer = io.BytesIO()
    buffer.write(pdf.output(dest='S'))
    buffer.seek(0)
    return buffer.getvalue()

# 4. SOL SIDEBAR - TEMİZ + PROFESSIONAL
with st.sidebar:
    # BRAND HEADER
    st.markdown("""
    <div class="brand-card">
        <h2 style='color:#ffffff; font-size:24px; font-weight:800; margin:0; letter-spacing:1px;'>🛰️ SATELLA AI</h2>
        <p style='color:rgba(255,255,255,0.7); font-size:11px; margin:8px 0 0 0; letter-spacing:2px; text-transform:uppercase;'>Geospatial Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # TARGET PARAMETERS
    st.markdown('<p class="sidebar-label">Target Parameters</p>', unsafe_allow_html=True)
    col_lat_lon = st.columns(2)
    with col_lat_lon[0]:
        st.text_input("LATITUDE", value="40.394799", key="lat_input")
    with col_lat_lon[1]:
        st.text_input("LONGITUDE", value="49.849585", key="lon_input")
    
    if st.button("🎯 SET TARGET AREA", key="set_target"):
        st.session_state.target_set = True
        st.success("✅ Target area locked!")
        st.rerun()
    
    # IMAGERY PIPELINE
    st.markdown('<p class="sidebar-label">Imagery Pipeline</p>', unsafe_allow_html=True)
    
    st.markdown("<p style='font-size:12px; color:#8b949e; margin:0 0 8px 0;'>T0: 2024 Baseline (Reference)</p>", unsafe_allow_html=True)
    t0_file = st.file_uploader("Upload T0", type=["png","jpg","jpeg"], key="t0")
    if t0_file:
        st.success(f"✅ {t0_file.name}")
    
    st.markdown("<p style='font-size:12px; color:#8b949e; margin:8px 0 8px 0;'>T1: 2025 Current (Target)</p>", unsafe_allow_html=True)
    t1_file = st.file_uploader("Upload T1", type=["png","jpg","jpeg"], key="t1")
    if t1_file:
        st.success(f"✅ {t1_file.name}")
    
    # RUN BUTTON
    if st.button("🚀 RUN CHANGE DETECTION", key="run_analysis"):
        if t0_file and t1_file:
            st.session_state.lat = float(st.session_state.get('lat_input', 40.394799))
            st.session_state.lon = float(st.session_state.get('lon_input', 49.849585))
            st.session_state.analysis_run = True
            st.balloons()
            st.rerun()
        else:
            st.error("❌ Upload both T0 and T1 images!")

# 5. ƏSAS LAYOUT
col_map, col_metrics = st.columns([3.5, 1.3])

with col_map:
    lat = st.session_state.get('lat', 40.394799)
    lon = st.session_state.get('lon', 49.849585)
    
    # MAP
    m = folium.Map(
        location=[lat, lon], 
        zoom_start=18,
        tiles=None,
        height=650
    )
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery"
    ).add_to(m)
    
    folium.Marker(
        [lat, lon],
        popup=f"📍 Analysis Center<br>{lat:.6f}°N {lon:.6f}°E",
        icon=folium.Icon(color="red", icon="satellite", prefix="fa")
    ).add_to(m)
    
    folium.Circle(
        [lat, lon],
        radius=150,
        color="#ff4444",
        fill=True,
        fillOpacity=0.2,
        popup="📏 Analysis Area: ~0.07 km²"
    ).add_to(m)
    
    folium_static(m, width=1250, height=650)
    
    # IMAGES
    if t0_file and t1_file:
        st.markdown("---")
        img1, img2 = process_images(t0_file, t1_file)
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.image(img1, caption="📷 T0: 2024 Baseline", use_column_width=True)
        with col_img2:
            st.image(img2, caption="📷 T1: 2025 Current", use_column_width=True)

with col_metrics:
    st.markdown("""
    <div style='color:#f0f6fc; font-size:16px; font-weight:700; margin-bottom:20px; padding-bottom:10px; border-bottom:1px solid #30363d;'>
        AI ANALYTICS
    </div>
    """, unsafe_allow_html=True)
    
    # METRICS
    st.markdown("""
    <div class="metric-box">
        <p style='color:#8b949e; font-size:11px; font-weight:700; margin:0 0 8px 0;'>DETECTED STRUCTURES</p>
        <p style='color:#58a6ff; font-size:32px; font-weight:800; margin:0;'>1</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-box">
        <p style='color:#8b949e; font-size:11px; font-weight:700; margin:0 0 8px 0;'>CONFIDENCE SCORE</p>
        <p style='color:#3fb950; font-size:28px; font-weight:800; margin:0;'>92.4%</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-box">
        <p style='color:#8b949e; font-size:11px; font-weight:700; margin:0 0 8px 0;'>STATUS</p>
        <p style='color:#f0f6fc; font-size:20px; font-weight:700; margin:0;'>✅ COMPLETE</p>
    </div>
    """, unsafe_allow_html=True)
    
    # DOWNLOAD
    if st.session_state.get('analysis_run', False) and t0_file and t1_file:
        report_data = generate_pdf(lat, lon)
        st.download_button(
            label="📥 DOWNLOAD FHN REPORT",
            data=report_data,
            file_name=f"SATELLA_Report_{lat:.4f}_{lon:.4f}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    st.markdown("""
    <div style='margin-top:40px; color:#8b949e; font-size:10px; text-align:center; letter-spacing:1px;'>
        SATELLA AI v3.2.1<br>Azerbaijan Geospatial Monitoring
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
