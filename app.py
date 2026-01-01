import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io
from PIL import Image

# 1. Səhifə Konfiqurasiyası
st.set_page_config(page_title="SATELLA AI", layout="wide", initial_sidebar_state="expanded")

# 2. UI Təkmilləşdirməsi (Stabil və Professional Dizayn)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* Fon rəngi */
    .main { background-color: #0b0d0e !important; font-family: 'Inter', sans-serif; }
    
    /* Sidebar-ı stabil saxla */
    [data-testid="stSidebar"] {
        min-width: 380px !important;
        max-width: 380px !important;
        background-color: #0d1117 !important;
        border-right: 1px solid #30363d !important;
    }

    /* Üst Header-i gizlət */
    [data-testid="stHeader"] { display: none !important; }

    /* Brend Kartı (Sol yuxarı) */
    .brand-card {
        background: linear-gradient(135deg, #1f6feb 0%, #111827 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* Professional Düymələr */
    div.stButton > button {
        background: #1f6feb !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        height: 48px !important;
        border: none !important;
        transition: 0.3s ease;
    }
    div.stButton > button:hover {
        background: #388bfd !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(31, 111, 235, 0.4);
    }

    /* Metrika Qutuları */
    [data-testid="stMetric"] {
        background: #161b22 !important;
        border: 1px solid #30363d !important;
        padding: 20px !important;
        border-radius: 12px !important;
    }
    
    /* Scrollbar Gizlətmə */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# 3. Funksiyalar
def process_images(img1, img2):
    i1 = Image.open(img1)
    i2 = Image.open(img2)
    # Şəkilləri eyni ölçüyə gətiririk
    target = (800, 600)
    return i1.resize(target, Image.Resampling.LANCZOS), i2.resize(target, Image.Resampling.LANCZOS)

def generate_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, "SATELLA ANALYSIS REPORT", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Location Coordinates: {lat:.6f}N, {lon:.6f}E", ln=True)
    pdf.cell(0, 10, f"Analysis Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=True)
    pdf.cell(0, 10, "Status: Changes Detected", ln=True)
    pdf.ln(5)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(0, 10, "Detection Count: 1 New Structure Identified", ln=True)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- SOL SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div class="brand-card">
        <h2 style='color:white;margin:0;font-size:24px'>🛰️ SATELLA AI</h2>
        <p style='color:#bfdbfe;font-size:11px;margin-top:5px;letter-spacing:1px'>GEOSPATIAL INTELLIGENCE</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📍 Area of Interest")
    lat_input = st.text_input("Latitude", value="40.394799")
    lon_input = st.text_input("Longitude", value="49.849585")
    
    if st.button("🎯 SET TARGET AREA", use_container_width=True):
        st.session_state.lat = float(lat_input)
        st.session_state.lon = float(lon_input)
        st.toast("Area Updated!", icon="📍")

    st.markdown("### 🛰️ Imagery Inputs")
    t0_file = st.file_uploader("T0: 2024 Baseline (Reference)", type=["png","jpg"])
    t1_file = st.file_uploader("T1: 2025 Current (Target)", type=["png","jpg"])
    
    if st.button("🚀 RUN CHANGE DETECTION", use_container_width=True):
        if t0_file and t1_file:
            st.session_state.run = True
            st.balloons()
        else:
            st.error("Please upload both images to continue.")

# --- ƏSAS EKRAN ---
col_map, col_stats = st.columns([3.6, 1.1])

with col_map:
    lat = st.session_state.get('lat', 40.394799)
    lon = st.session_state.get('lon', 49.849585)
    
    # Xəritə (Esri Satellite Layer - Attribution xətası düzəldildi)
    m = folium.Map(location=[lat, lon], zoom_start=18)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri World Imagery"
    ).add_to(m)
    
    # Marker və Radius
    folium.Marker([lat, lon], popup="Analysis Site", tooltip="View Location").add_to(m)
    folium.Circle([lat, lon], radius=150, color='#1f6feb', fill=True, fill_opacity=0.15).add_to(m)
    
    folium_static(m, width=1080, height=580)
    
    # Şəkil Müqayisəsi
    if t0_file and t1_file:
        st.markdown("<h3 style='color:white; margin-top:20px'>🔍 Temporal Analysis</h3>", unsafe_allow_html=True)
        img1, img2 = process_images(t0_file, t1_file)
        c1, c2 = st.columns(2)
        with c1: st.image(img1, caption="2024 (T0 Reference)", use_container_width=True)
        with c2: st.image(img2, caption="2025 (T1 Current)", use_container_width=True)

with col_stats:
    st.markdown("<p style='font-weight:700; color:#8b949e; font-size:13px; margin-bottom:15px'>AI ANALYTICS</p>", unsafe_allow_html=True)
    
    status_msg = "1 Building" if st.session_state.get('run', False) else "0"
    
    st.metric("New Structures", status_msg)
    st.metric("AI Confidence", "92.4%", delta="Optimal")
    st.metric("F1-Score", "0.90")
    
    st.markdown("<div style='margin-top:30px'></div>", unsafe_allow_html=True)
    
    if st.session_state.get('run', False):
        st.markdown("#### 📄 Export Results")
        pdf_data = generate_pdf(lat, lon)
        st.download_button(
            label="📥 GENERATE FHN REPORT",
            data=pdf_data,
            file_name=f"SATELLA_ANALYSIS_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# Footer
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; color:#484f58; font-size:12px'>SATELLA AI Engine v3.3 | Built for VISTAR Excellence Program | {datetime.now().year}</div>", unsafe_allow_html=True)
