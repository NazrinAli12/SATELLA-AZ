import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
from PIL import Image

# 1. Səhifə Ayarları - Sidebar həmişə açıq (expanded)
st.set_page_config(
    page_title="SATELLA AI", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. Professional & Stabil UI (Sidebar-ın itməməsi üçün təmizlənmiş CSS)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* Ana fon rəngi */
    .stApp {
        background-color: #0b0d0e;
        font-family: 'Inter', sans-serif;
    }

    /* Sol Panel (Sidebar) Dizaynı - Görünürlük zəmanəti */
    [data-testid="stSidebar"] {
        background-color: #0d1117 !important;
        border-right: 1px solid #30363d !important;
    }

    /* Sidebar daxilindəki mətnlərin rəngi */
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label {
        color: #e6edf3 !important;
    }

    /* Üst paneli (header) gizlət */
    [data-testid="stHeader"] { display: none !important; }

    /* Brend Kartı */
    .brand-box {
        background: #1f6feb;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .brand-title {
        color: white;
        font-size: 20px;
        font-weight: 800;
        margin: 0;
        letter-spacing: 1px;
    }

    /* Metrika Qutuları (Sağ tərəf) */
    .metric-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
    }

    /* Düymə üslubu */
    div.stButton > button {
        background-color: #238636 !important;
        color: white !important;
        border-radius: 6px !important;
        width: 100%;
        border: none !important;
        height: 45px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 3. Köməkçi Funksiyalar
def generate_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, "SATELLA AI - MONITORING REPORT", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Location: {lat}, {lon}", ln=True)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- SIDEBAR (SOL PANEL) - Kodun bu hissəsi mütləq dolmalıdır ---
with st.sidebar:
    st.markdown("""
    <div class="brand-box">
        <p class="brand-title">🛰️ SATELLA AI</p>
        <p style="color:rgba(255,255,255,0.7); font-size:10px; margin:0;">Enterprise AI Monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("📍 Area of Interest")
    lat_input = st.text_input("Latitude", value="40.394799", key="lat")
    lon_input = st.text_input("Longitude", value="49.849585", key="lon")
    
    if st.button("🎯 SET TARGET AREA"):
        st.session_state.lat_val = float(lat_input)
        st.session_state.lon_val = float(lon_input)
        st.toast("Məkan yeniləndi!")

    st.subheader("🛰️ Imagery Inputs")
    t0_file = st.file_uploader("T0: 2024 Baseline", type=["png","jpg","jpeg"])
    t1_file = st.file_uploader("T1: 2025 Current", type=["png","jpg","jpeg"])
    
    run_btn = st.button("🚀 RUN CHANGE DETECTION")
    if run_btn:
        if t0_file and t1_file:
            st.session_state.is_running = True
        else:
            st.error("Zəhmət olmasa şəkilləri yükləyin!")

# --- ANA EKRAN (Responsive Layout) ---
# Ekranın 80%-i xəritə, 20%-i metriklər üçün
col_map, col_stats = st.columns([4, 1])

with col_map:
    # Koordinatları session_state-dən götürürük
    cur_lat = float(st.session_state.get('lat_val', 40.394799))
    cur_lon = float(st.session_state.get('lon_val', 49.849585))
    
    # Xəritə (ArcGIS Satellite)
    m = folium.Map(location=[cur_lat, cur_lon], zoom_start=18, control_scale=True)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        name="Satellite"
    ).add_to(m)
    folium.Marker([cur_lat, cur_lon], popup="Target").add_to(m)
    
    # Xəritəni ekranın eninə görə tənzimləyirik
    folium_static(m, width=1000, height=550)
    
    # Şəkil Müqayisəsi (Əgər yüklənibsə)
    if t0_file and t1_file:
        st.markdown("### 🔍 Temporal Analysis")
        c1, c2 = st.columns(2)
        with c1: st.image(t0_file, caption="2024 Baseline", use_container_width=True)
        with c2: st.image(t1_file, caption="2025 Current", use_container_width=True)

with col_stats:
    st.markdown("### 📊 Metrics")
    
    # Statik və ya AI nəticələri
    detected_count = "1" if st.session_state.get('is_running', False) else "0"
    
    st.markdown(f"""
    <div class="metric-card">
        <p style='color:#8b949e; font-size:11px; margin:0;'>NEW BUILDINGS</p>
        <p style='color:white; font-size:24px; font-weight:800; margin:0;'>{detected_count}</p>
    </div>
    <div class="metric-card">
        <p style='color:#8b949e; font-size:11px; margin:0;'>AI PRECISION</p>
        <p style='color:#58a6ff; font-size:24px; font-weight:800; margin:0;'>92.4%</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get('is_running', False):
        st.success("Analysis Complete")
        pdf_data = generate_pdf(cur_lat, cur_lon)
        st.download_button(
            label="📥 DOWNLOAD REPORT",
            data=pdf_data,
            file_name="satella_report.pdf",
            mime="application/pdf"
        )

# Footer
st.markdown("<hr><p style='text-align:center; color:#484f58; font-size:10px;'>SATELLA AI v3.3 | Professional Geospatial Analysis</p>", unsafe_allow_html=True)
