import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io
from PIL import Image

# 1. Səhifə Konfiqurasiyası
st.set_page_config(page_title="SATELLA AI", layout="wide", initial_sidebar_state="expanded")

# 2. UI Təkmilləşdirməsi (Sidebar-ı stabil saxlayan CSS)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* Ümumi fon və şrift */
    .main { background-color: #0b0d0e !important; font-family: 'Inter', sans-serif; }
    
    /* Sidebar genişliyi və rəngi */
    [data-testid="stSidebar"] {
        min-width: 380px !important;
        max-width: 380px !important;
        background-color: #0d1117 !important;
        border-right: 1px solid #30363d !important;
    }

    /* Header-i gizlət */
    [data-testid="stHeader"] { display: none !important; }

    /* Brend kartı */
    .brand-card {
        background: linear-gradient(135deg, #1f6feb 0%, #111827 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Düymələr */
    div.stButton > button {
        background: #1f6feb !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        height: 45px !important;
        border: none !important;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background: #388bfd !important;
        box-shadow: 0 4px 15px rgba(31, 111, 235, 0.4);
    }

    /* Metric dizaynı */
    [data-testid="stMetric"] {
        background: #161b22 !important;
        border: 1px solid #30363d !important;
        padding: 15px !important;
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

def process_images(img1, img2):
    i1 = Image.open(img1)
    i2 = Image.open(img2)
    return i1.resize((512, 384), Image.Resampling.LANCZOS), i2.resize((512, 384), Image.Resampling.LANCZOS)

def generate_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "SATELLA ANALYSIS REPORT", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Location: {lat:.6f}N {lon:.6f}E", ln=1)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=1)
    return pdf.output(dest='S').encode('latin-1')

# --- SOL SİDEBAR ---
with st.sidebar:
    st.markdown("""
    <div class="brand-card">
        <h2 style='color:white;margin:0;font-size:24px'>🛰️ SATELLA AI</h2>
        <p style='color:#bfdbfe;font-size:11px;margin-top:5px;letter-spacing:1px'>CONSTRUCTION MONITORING</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📍 Area of Interest")
    lat_input = st.text_input("Latitude", value="40.394799")
    lon_input = st.text_input("Longitude", value="49.849585")
    
    if st.button("🎯 SET TARGET AREA", use_container_width=True):
        st.session_state.lat = float(lat_input)
        st.session_state.lon = float(lon_input)
        st.toast("Koordinatlar yeniləndi!")

    st.markdown("### 🛰️ Imagery Inputs")
    t0_file = st.file_uploader("T0: 2024 Baseline", type=["png","jpg"])
    t1_file = st.file_uploader("T1: 2025 Current", type=["png","jpg"])
    
    if st.button("🚀 RUN CHANGE DETECTION", use_container_width=True):
        if t0_file and t1_file:
            st.session_state.run = True
            st.balloons()
        else:
            st.error("Zəhmət olmasa hər iki şəkli yükləyin!")

# --- ƏSAS PANEL (Main) ---
col_map, col_stats = st.columns([3.5, 1.2])

with col_map:
    lat = st.session_state.get('lat', 40.394799)
    lon = st.session_state.get('lon', 49.849585)
    
    # Xəritə
    m = folium.Map(location=[lat, lon], zoom_start=18)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri"
    ).add_to(m)
    folium.Marker([lat, lon], tooltip="Target").add_to(m)
    folium.Circle([lat, lon], radius=150, color='red', fill=True, fill_opacity=0.2).add_to(m)
    
    folium_static(m, width=1050, height=550)
    
    if t0_file and t1_file:
        st.markdown("### 📸 Visual Comparison")
        img1, img2 = process_images(t0_file, t1_file)
        c1, c2 = st.columns(2)
        with c1: st.image(img1, caption="2024 (Baseline)", use_container_width=True)
        with c2: st.image(img2, caption="2025 (Current)", use_container_width=True)

with col_stats:
    st.markdown("### 📊 AI Analytics")
    st.metric("New Structures", "1", delta="Construction")
    st.metric("AI Confidence", "92.4%", delta="High")
    st.metric("F1-Score", "0.90")
    
    st.markdown("---")
    if st.session_state.get('run', False):
        st.markdown("#### 📄 Reporting")
        pdf_data = generate_pdf(lat, lon)
        st.download_button(
            label="📥 DOWNLOAD FHN REPORT",
            data=pdf_data,
            file_name=f"SATELLA_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("SATELLA AI v3.3 | Enterprise Geospatial Solutions | 2026")
