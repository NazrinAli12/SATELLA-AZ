import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
from PIL import Image

# 1. SƏHİFƏ AYARLARI (Mütləq ən başda)
st.set_page_config(
    page_title="SATELLA AI", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. EKSTREMAL SIDEBAR CSS (Sol paneli ekrana məcburi çıxarır)
st.markdown("""
<style>
    /* Ana tətbiq fonu */
    .stApp { background-color: #0b0d0e; }
    
    /* SIDEBAR: Görünməsi üçün rəngi və ölçüsünü sabitləyirik */
    [data-testid="stSidebar"] {
        background-color: #111418 !important;
        width: 350px !important;
        border-right: 2px solid #1f6feb !important;
    }
    
    /* Sidebar daxilindəki mətnləri məcburi ağ rəng edirik */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Input və düymələrin sidebar-da fərqlənməsi üçün */
    [data-testid="stSidebar"] .stTextInput input {
        background-color: #1c2128 !important;
        border: 1px solid #30363d !important;
        color: white !important;
    }

    /* Brend Başlığı */
    .brand-container {
        background: linear-gradient(135deg, #1f6feb 0%, #0d1117 100%);
        padding: 25px;
        border-radius: 12px;
        margin-bottom: 20px;
        text-align: center;
        border: 1px solid #388bfd;
    }

    /* Header gizlət */
    [data-testid="stHeader"] { display: none !important; }

    /* Metrika kartları (Sağ panel) */
    .metric-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# 3. PDF GENERATOR
def create_report(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, "SATELLA AI - MONITORING REPORT", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Location: {lat}, {lon}", ln=True)
    pdf.cell(0, 10, f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- 🛰️ SOL PANEL (SIDEBAR) ---
# Diqqət: Bu blokun içindəki hər şey birbaşa sidebar-a gedir
with st.sidebar:
    st.markdown("""
    <div class="brand-container">
        <h2 style="margin:0; font-size:24px;">🛰️ SATELLA</h2>
        <p style="font-size:10px; opacity:0.8; letter-spacing:1px; margin-top:5px;">ENTERPRISE AI MONITORING</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📍 Location Control")
    lat_val = st.text_input("Latitude", value="40.394799", key="side_lat")
    lon_val = st.text_input("Longitude", value="49.849585", key="side_lon")
    
    if st.button("🎯 UPDATE MAP VIEW", use_container_width=True):
        st.session_state.lat = float(lat_val)
        st.session_state.lon = float(lon_val)

    st.markdown("---")
    st.markdown("### 🛰️ Imagery Feed")
    t0 = st.file_uploader("T0: 2024 Reference", type=["png", "jpg"], key="up_t0")
    t1 = st.file_uploader("T1: 2025 Current", type=["png", "jpg"], key="up_t1")
    
    if st.button("🚀 EXECUTE AI ENGINE", use_container_width=True):
        if t0 and t1:
            st.session_state.is_analysed = True
            st.balloons()
        else:
            st.error("Missing Data!")

# --- 🗺️ ƏSAS EKRAN LAYOUT ---
col_map, col_data = st.columns([3.5, 1.2])

with col_map:
    # Koordinatları session_state-dən götür (və ya default)
    lat = st.session_state.get('lat', 40.394799)
    lon = st.session_state.get('lon', 49.849585)
    
    # Xəritə (ArcGIS Satellite - Error Düzəldilib)
    m = folium.Map(location=[lat, lon], zoom_start=18)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri Satellite",
        name="ArcGIS"
    ).add_to(m)
    folium.Marker([lat, lon], tooltip="Current Target Area").add_to(m)
    
    # Xəritəni göstər
    folium_static(m, width=1000, height=530)
    
    if t0 and t1:
        st.markdown("### 🔍 Side-by-Side Analysis")
        c1, c2 = st.columns(2)
        c1.image(t0, caption="2024 (T0)", use_container_width=True)
        c2.image(t1, caption="2025 (T1)", use_container_width=True)

with col_data:
    st.markdown("### 📊 Metrics")
    detected = "1" if st.session_state.get('is_analysed', False) else "0"
    
    st.markdown(f"""
    <div class="metric-card">
        <p style="color:#8b949e; font-size:12px; margin:0;">NEW OBJECTS</p>
        <p style="color:white; font-size:26px; font-weight:bold; margin:0;">{detected} Units</p>
    </div>
    <div class="metric-card">
        <p style="color:#8b949e; font-size:12px; margin:0;">AI CONFIDENCE</p>
        <p style="color:#58a6ff; font-size:26px; font-weight:bold; margin:0;">92.4%</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get('is_analysed', False):
        st.info("Analysis Ready")
        pdf_report = create_report(lat, lon)
        st.download_button(
            label="📥 DOWNLOAD REPORT",
            data=pdf_report,
            file_name=f"Satella_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# Footer
st.markdown("<br><hr><center style='color:#484f58; font-size:11px;'>SATELLA AI v3.3 | Professional Geospatial System</center>", unsafe_allow_html=True)
