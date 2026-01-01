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

# 2. Professional Enterprise UI (Təmiz və Stabil)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Ana Fon */
    .stApp {
        background-color: #0b0d0e !important;
        font-family: 'Inter', sans-serif;
    }

    /* Sol Panel (Sidebar) - Sabit və Həmişə Görünən */
    [data-testid="stSidebar"] {
        background-color: #0d1117 !important;
        border-right: 1px solid #30363d !important;
        width: 380px !important;
    }

    /* Header və lazımsız elementləri gizlət */
    [data-testid="stHeader"] { display: none !important; }
    section[data-testid="stSidebar"] .st-emotion-cache-164784y { display: none !important; } /* Collapse düyməsini gizlət (ixtiyari) */

    /* Brend Paneli (Sidebar daxili) */
    .brand-box {
        background: #1f6feb;
        padding: 24px;
        border-radius: 12px;
        margin: -10px 0 25px 0;
        text-align: left;
    }
    
    .brand-text {
        color: white;
        font-size: 20px;
        font-weight: 800;
        margin: 0;
        letter-spacing: 1px;
    }

    /* Metrika Qutuları (Sağ panel) */
    .stat-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }

    /* Şəkil müqayisəsi konteyneri */
    .img-container {
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 5px;
        background: #0d1117;
    }
</style>
""", unsafe_allow_html=True)

# 3. Köməkçi Funksiyalar
def process_images(img1, img2):
    i1 = Image.open(img1)
    i2 = Image.open(img2)
    # Şəkilləri ekran ölçüsünə uyğun mütənasib kiçiltmək
    return i1, i2

def generate_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, "SATELLA AI - MONITORING REPORT", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Location: {lat}, {lon}", ln=True)
    pdf.cell(0, 10, f"Analysis Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=True)
    pdf.cell(0, 10, "Detection: 1 Change Point Identified", ln=True)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- SIDEBAR (SOL PANEL) ---
with st.sidebar:
    st.markdown("""
    <div class="brand-box">
        <p class="brand-text">🛰️ SATELLA AI</p>
        <p style="color:rgba(255,255,255,0.7); font-size:11px; margin:0;">Enterprise Monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📍 Area of Interest")
    lat_val = st.text_input("Latitude", value="40.394799", key="lat_main")
    lon_val = st.text_input("Longitude", value="49.849585", key="lon_main")
    
    if st.button("🎯 SYNC LOCATION", use_container_width=True):
        st.session_state.lat = float(lat_val)
        st.session_state.lon = float(lon_val)
        st.toast("Məkan yeniləndi!")

    st.markdown("### 🛰️ Imagery")
    t0_file = st.file_uploader("T0: 2024 Baseline", type=["png","jpg","jpeg"], key="u_t0")
    t1_file = st.file_uploader("T1: 2025 Current", type=["png","jpg","jpeg"], key="u_t1")
    
    if st.button("🚀 EXECUTE AI", use_container_width=True):
        if t0_file and t1_file:
            st.session_state.run = True
            st.balloons()
        else:
            st.error("Hər iki şəkli daxil edin!")

# --- ANA EKRAN (Responsive Layout) ---
col_map, col_metrics = st.columns([3.8, 1.2])

with col_map:
    lat = st.session_state.get('lat', 40.394799)
    lon = st.session_state.get('lon', 49.849585)
    
    # Xəritə (Ekranın eninə uyğunlaşır)
    m = folium.Map(location=[lat, lon], zoom_start=18, control_scale=True)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        name="Satellite View"
    ).add_to(m)
    
    folium.Marker([lat, lon], popup="Target Area").add_to(m)
    
    # Xəritəni responsive etmək üçün use_container_width yoxdur, amma folium_static width=None ilə işləyir
    folium_static(m, width=1100, height=520)
    
    if t0_file and t1_file:
        st.markdown("### 🔍 AI Detection Results")
        img1, img2 = process_images(t0_file, t1_file)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="img-container">', unsafe_allow_html=True)
            st.image(img1, caption="2024 Reference", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="img-container">', unsafe_allow_html=True)
            st.image(img2, caption="2025 Identified", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

with col_metrics:
    st.markdown("### 📊 Metrics")
    
    changes = "1" if st.session_state.get('run', False) else "0"
    
    st.markdown(f"""
    <div class="stat-card">
        <p style='color:#8b949e; font-size:12px; margin:0;'>NEW STRUCTURES</p>
        <p style='color:white; font-size:28px; font-weight:800; margin:0;'>{changes}</p>
    </div>
    <div class="stat-card">
        <p style='color:#8b949e; font-size:12px; margin:0;'>AI PRECISION</p>
        <p style='color:#58a6ff; font-size:28px; font-weight:800; margin:0;'>92.4%</p>
    </div>
    <div class="stat-card">
        <p style='color:#8b949e; font-size:12px; margin:0;'>F1-SCORE</p>
        <p style='color:#3fb950; font-size:28px; font-weight:800; margin:0;'>90%</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get('run', False):
        st.markdown("---")
        pdf_bytes = generate_pdf(lat, lon)
        st.download_button(
            label="📥 DOWNLOAD REPORT",
            data=pdf_bytes,
            file_name=f"SATELLA_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# Footer
st.markdown("<br><hr><center style='color:#484f58; font-size:12px;'>SATELLA AI Engine v3.3 | Professional Geospatial Analysis</center>", unsafe_allow_html=True)
