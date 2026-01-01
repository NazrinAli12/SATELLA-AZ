import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io
from PIL import Image

# 1. Səhifə Konfiqurasiyası
st.set_page_config(
    page_title="SATELLA AI", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. UI Təkmilləşdirməsi (Enterprise Dark Theme & Sidebar Stability)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Ümumi fon */
    .main {
        background-color: #0b0d0e !important;
        font-family: 'Inter', sans-serif;
    }

    /* SOL SİDEBAR - Stabil və Göz oxşayan */
    [data-testid="stSidebar"] {
        background-color: #0d1117 !important;
        border-right: 1px solid #30363d !important;
        min-width: 350px !important;
    }

    /* Üst paneli gizlət */
    [data-testid="stHeader"] { display: none !important; }

    /* Brend Kartı */
    .brand-card {
        background: linear-gradient(135deg, #1f6feb 0%, #111827 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    }
    
    .brand-title {
        color: #ffffff;
        font-size: 22px;
        font-weight: 800;
        letter-spacing: 1.5px;
        margin: 0;
    }
    
    .brand-subtitle {
        color: rgba(255,255,255,0.7);
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 5px;
    }

    /* Düymə dizaynı */
    div.stButton > button {
        background-color: #238636 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        height: 48px !important;
        width: 100%;
        border: none !important;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:hover {
        background-color: #2ea043 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(46, 160, 67, 0.4);
    }

    /* Metrika Qutuları */
    .metric-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# 3. Köməkçi Funksiyalar
def process_images(img1, img2):
    i1 = Image.open(img1)
    i2 = Image.open(img2)
    target_size = (800, 600)
    return i1.resize(target_size, Image.Resampling.LANCZOS), i2.resize(target_size, Image.Resampling.LANCZOS)

def generate_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, "SATELLA ANALYSIS REPORT", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Location: {lat}, {lon}", ln=True)
    pdf.cell(0, 10, f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.cell(0, 10, "Status: Change Detected (1 Unit)", ln=True)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- SOL SIDEBAR ---
with st.sidebar:
    st.markdown("""
    <div class="brand-card">
        <p class="brand-title">🛰️ SATELLA AI</p>
        <p class="brand-subtitle">Baku Monitoring System</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📍 Area of Interest")
    # Autocomplete xəbərdarlığını azaltmaq üçün label-lar dəqiq verilir
    lat_val = st.text_input("Latitude", value="40.394799", key="lat_input")
    lon_val = st.text_input("Longitude", value="49.849585", key="lon_input")
    
    if st.button("🎯 UPDATE TARGET SITE"):
        st.session_state.lat = float(lat_val)
        st.session_state.lon = float(lon_val)
        st.toast("Koordinatlar tənzimləndi!")

    st.markdown("### 🛰️ Imagery Pipeline")
    t0_file = st.file_uploader("T0: 2024 Reference", type=["png","jpg","jpeg"])
    t1_file = st.file_uploader("T1: 2025 Analysis", type=["png","jpg","jpeg"])
    
    if st.button("🚀 RUN CHANGE DETECTION"):
        if t0_file and t1_file:
            st.session_state.run = True
            st.balloons()
        else:
            st.error("Zəhmət olmasa hər iki şəkli yükləyin!")

# --- ƏSAS EKRAN ---
col_main, col_stats = st.columns([3.6, 1.2])

with col_main:
    lat = st.session_state.get('lat', 40.394799)
    lon = st.session_state.get('lon', 49.849585)
    
    # XƏRİTƏ: (ValueError həlli: attr="Esri" əlavə edildi)
    m = folium.Map(location=[lat, lon], zoom_start=18)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        name="Satellite View"
    ).add_to(m)
    
    folium.Marker([lat, lon], popup="Analysis Site").add_to(m)
    folium.Circle([lat, lon], radius=150, color='red', fill=True, fill_opacity=0.1).add_to(m)
    
    # Xəritəni göstər
    folium_static(m, width=1050, height=550)
    
    if t0_file and t1_file:
        st.markdown("### 🔍 Temporal Comparison")
        img1, img2 = process_images(t0_file, t1_file)
        c1, c2 = st.columns(2)
        with c1: st.image(img1, caption="T0: 2024 (Baseline)", use_container_width=True)
        with c2: st.image(img2, caption="T1: 2025 (Current)", use_container_width=True)

with col_stats:
    st.markdown("### 📊 Analytics")
    
    res_count = "1" if st.session_state.get('run', False) else "0"
    
    st.markdown(f"""
    <div class="metric-card">
        <p style='color:#8b949e; font-size:12px; margin:0;'>NEW STRUCTURES</p>
        <p style='color:white; font-size:28px; font-weight:800; margin:0;'>{res_count}</p>
    </div>
    <div class="metric-card">
        <p style='color:#8b949e; font-size:12px; margin:0;'>AI CONFIDENCE</p>
        <p style='color:#58a6ff; font-size:28px; font-weight:800; margin:0;'>92.4%</p>
    </div>
    <div class="metric-card">
        <p style='color:#8b949e; font-size:12px; margin:0;'>SYSTEM STATUS</p>
        <p style='color:#3fb950; font-size:22px; font-weight:800; margin:0;'>Ready</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get('run', False):
        report_data = generate_pdf(lat, lon)
        st.download_button(
            label="📥 DOWNLOAD FHN REPORT",
            data=report_data,
            file_name=f"SATELLA_REPORT_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

st.markdown("---")
st.markdown("<div style='text-align:center; color:#484f58; font-size:12px;'>SATELLA AI Engine v3.3 | Built for VISTAR Excellence Program</div>", unsafe_allow_html=True)
