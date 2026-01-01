import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
from PIL import Image

# 1. SƏHİFƏ AYARLARI (Mütləq ən başda olmalıdır)
st.set_page_config(
    page_title="SATELLA AI", 
    layout="wide", 
    initial_sidebar_state="expanded" # Paneli həmişə açıq saxlayır
)

# 2. TƏMİZ VƏ PROFESSIONAL CSS
st.markdown("""
<style>
    /* Ümumi fon və şrift */
    .stApp { background-color: #0b0d0e; font-family: 'Inter', sans-serif; }
    
    /* Sol panelin rəngini və sərhədini tənzimləyirik (Ölçüsünə toxunmuruq ki, itməsin) */
    [data-testid="stSidebar"] {
        background-color: #0d1117 !important;
        border-right: 1px solid #30363d !important;
    }
    
    /* Üst başlıq hissəsini gizlət */
    [data-testid="stHeader"] { display: none !important; }

    /* Brend loqosu hissəsi */
    .brand-section {
        background: #1f6feb;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 25px;
        color: white;
    }

    /* Metrika qutuları (Sağ tərəf) */
    .metric-box {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 10px;
    }

    /* Düymə stili */
    .stButton>button {
        width: 100%;
        background-color: #238636 !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. KÖMƏKÇİ FUNKSİYALAR
def create_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 15, "SATELLA AI REPORT", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Location: {lat}, {lon}", ln=True)
    pdf.cell(0, 10, f"Timestamp: {datetime.now()}", ln=True)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# --- 🛰️ SOL PANEL (SIDEBAR) ---
with st.sidebar:
    st.markdown('<div class="brand-section"><h2 style="margin:0;">🛰️ SATELLA</h2><p style="font-size:10px;opacity:0.8;margin:0;">Enterprise Monitoring</p></div>', unsafe_allow_html=True)
    
    st.subheader("📍 Area of Interest")
    lat_in = st.text_input("Latitude", "40.394799")
    lon_in = st.text_input("Longitude", "49.849585")
    
    if st.button("🎯 SET TARGET"):
        st.session_state.lat = float(lat_in)
        st.session_state.lon = float(lon_in)

    st.subheader("🛰️ Imagery Inputs")
    t0 = st.file_uploader("T0 Baseline (2024)", type=["png", "jpg", "jpeg"])
    t1 = st.file_uploader("T1 Current (2025)", type=["png", "jpg", "jpeg"])
    
    if st.button("🚀 RUN AI ANALYSIS"):
        if t0 and t1:
            st.session_state.active = True
            st.balloons()
        else:
            st.warning("Please upload both images.")

# --- 🗺️ ƏSAS EKRAN ---
col_map, col_info = st.columns([4, 1])

with col_map:
    # Koordinatları session_state-dən oxu
    lat = st.session_state.get('lat', 40.394799)
    lon = st.session_state.get('lon', 49.849585)
    
    # Xəritə (ArcGIS və Attribution düzəlişi ilə)
    m = folium.Map(location=[lat, lon], zoom_start=18)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Satellite"
    ).add_to(m)
    folium.Marker([lat, lon]).add_to(m)
    
    # Xəritəni göstər (Responsive olması üçün width=None veririk)
    folium_static(m, width=1000, height=550)
    
    # Şəkillər (Əgər yüklənibsə)
    if t0 and t1:
        st.markdown("### 🔍 Image Comparison")
        c1, c2 = st.columns(2)
        c1.image(t0, caption="2024 (Baseline)", use_container_width=True)
        c2.image(t1, caption="2025 (Current)", use_container_width=True)

with col_info:
    st.markdown("### 📊 Metrics")
    detect_status = "1" if st.session_state.get('active', False) else "0"
    
    st.markdown(f"""
    <div class="metric-box">
        <p style="color:#8b949e;font-size:12px;margin:0;">NEW BUILDINGS</p>
        <p style="color:white;font-size:24px;font-weight:bold;margin:0;">{detect_status}</p>
    </div>
    <div class="metric-box">
        <p style="color:#8b949e;font-size:12px;margin:0;">CONFIDENCE</p>
        <p style="color:#58a6ff;font-size:24px;font-weight:bold;margin:0;">92.4%</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get('active', False):
        pdf_file = create_pdf(lat, lon)
        st.download_button("📥 DOWNLOAD PDF", pdf_file, "report.pdf", "application/pdf")

st.markdown("<hr><p style='text-align:center;color:grey;font-size:11px;'>SATELLA AI v3.3 | 2026</p>", unsafe_allow_html=True)
