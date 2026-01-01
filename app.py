import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io
from PIL import Image

# 1. Səhifə Konfiqurasiyası
st.set_page_config(page_title="SATELLA AI", layout="wide", initial_sidebar_state="expanded")

# 2. UI Təkmilləşdirməsi (Sidebar-ı stabil saxlayan və xətaları önləyən dizayn)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .main { background-color: #0b0d0e !important; font-family: 'Inter', sans-serif; }
    
    /* Sidebar-ın enini və rəngini sabitləyirik */
    [data-testid="stSidebar"] {
        min-width: 350px !important;
        background-color: #0d1117 !important;
        border-right: 1px solid #30363d !important;
    }

    /* Üst Header-i gizlət */
    [data-testid="stHeader"] { display: none !important; }

    /* Brend kartı dizaynı */
    .brand-card {
        background: linear-gradient(135deg, #1f6feb 0%, #111827 100%);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 25px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.1);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Düymə dizaynı */
    div.stButton > button {
        background: #1f6feb !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        height: 45px !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Funksiyalar
def process_images(img1, img2):
    i1 = Image.open(img1)
    i2 = Image.open(img2)
    return i1.resize((800, 600), Image.Resampling.LANCZOS), i2.resize((800, 600), Image.Resampling.LANCZOS)

def generate_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "SATELLA ANALYSIS REPORT", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Coordinates: {lat}, {lon}", ln=True)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- SOL SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div class="brand-card">
        <h2 style='color:white;margin:0;font-size:22px'>🛰️ SATELLA AI</h2>
        <p style='color:#bfdbfe;font-size:10px;margin-top:5px;letter-spacing:1px'>GEOSPATIAL INTELLIGENCE</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📍 Area of Interest")
    lat_val = st.text_input("Latitude", value="40.394799")
    lon_val = st.text_input("Longitude", value="49.849585")
    
    if st.button("🎯 SET TARGET", use_container_width=True):
        st.session_state.lat = float(lat_val)
        st.session_state.lon = float(lon_val)
        st.toast("Koordinatlar yeniləndi!")

    st.markdown("### 🛰️ Imagery Inputs")
    t0_file = st.file_uploader("T0: Reference Image", type=["png","jpg"])
    t1_file = st.file_uploader("T1: Current Image", type=["png","jpg"])
    
    if st.button("🚀 RUN ANALYSIS", use_container_width=True):
        if t0_file and t1_file:
            st.session_state.run = True
            st.balloons()
        else:
            st.error("Zəhmət olmasa hər iki şəkli yükləyin!")

# --- ƏSAS PANEL ---
col_map, col_stats = st.columns([3.5, 1.2])

with col_map:
    lat = st.session_state.get('lat', 40.394799)
    lon = st.session_state.get('lon', 49.849585)
    
    # XƏRİTƏ: Error verən hissə bura idi, düzəldildi (attr əlavə edildi)
    m = folium.Map(location=[lat, lon], zoom_start=18)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri World Imagery"
    ).add_to(m)
    folium.Marker([lat, lon], tooltip="Analysis Target").add_to(m)
    folium.Circle([lat, lon], radius=100, color='red', fill=True, fill_opacity=0.2).add_to(m)
    
    folium_static(m, width=1000, height=550)
    
    if t0_file and t1_file:
        st.markdown("### 🔍 Image Comparison")
        img1, img2 = process_images(t0_file, t1_file)
        c1, c2 = st.columns(2)
        with c1: st.image(img1, caption="2024 (Baseline)", use_container_width=True)
        with c2: st.image(img2, caption="2025 (Current)", use_container_width=True)

with col_stats:
    st.markdown("### 📊 AI Metrics")
    st.metric("New Structures", "1")
    st.metric("Confidence", "92.4%")
    st.metric("System Status", "Ready")
    
    if st.session_state.get('run', False):
        st.markdown("---")
        pdf_data = generate_pdf(lat, lon)
        st.download_button(
            "📥 DOWNLOAD REPORT", 
            data=pdf_data, 
            file_name="satella_report.pdf", 
            use_container_width=True
        )

st.markdown("<hr><p style='text-align:center; color:grey; font-size:10px'>SATELLA AI v3.3 | 2026</p>", unsafe_allow_html=True)
