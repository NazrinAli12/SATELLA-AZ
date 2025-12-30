import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io

# 1. Page Config
st.set_page_config(page_title="SATELLA", layout="wide", initial_sidebar_state="expanded")

# 2. Advanced UI Styling (Yığcam Sol Panel + No Scroll)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #0b0d0e !important;
        overflow: hidden !important;
    }

    /* SOL SİDEBAR - Yığcam və Scroll-suz */
    section[data-testid="stSidebar"] {
        width: 380px !important;
        background-color: #111418 !important;
        border-right: 1px solid #2d333b !important;
    }
    section[data-testid="stSidebar"] > div {
        height: 100vh !important;
        overflow: hidden !important;
        padding: 1.5rem 1rem !important; /* Padding azaldıldı */
    }

    /* Elementlər arasındakı boşluğu sıxmaq */
    [data-testid="stVerticalBlock"] { gap: 0.5rem !important; }

    /* SAĞ PANEL */
    [data-testid="column"]:nth-child(2) {
        background-color: #111418 !important;
        border-left: 1px solid #2d333b !important;
        padding: 20px !important;
        height: 100vh;
    }

    /* SCROLLBAR LƏĞVİ */
    ::-webkit-scrollbar { display: none !important; }

    /* Düymə və Kart Stili */
    div.stButton > button {
        background: #1a73e8 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        height: 40px !important;
    }
    .metric-card {
        background: #1a1f24;
        border: 1px solid #3c4043;
        border-radius: 10px;
        padding: 12px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# 3. PDF Generator
def generate_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "SATELLA FHN Report", ln=1, align='C')
    return pdf.output(dest='S').encode('latin-1')

# --- SOL SIDEBAR (YIĞCAM) ---
with st.sidebar:
    # Header - Daha kiçik padding
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1e3a8a,#3b82f6);padding:1rem;border-radius:10px;margin-bottom:1rem'>
        <h2 style='color:white;margin:0;font-size:20px;'>🛰️ SATELLA</h2>
        <p style='color:#bfdbfe;margin:0;font-size:11px'>Construction Monitor</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Target Settings
    st.markdown("<p style='font-size:12px; font-weight:700; color:#9ca3af; margin-bottom:2px'>AREA CONTROL</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: lat_val = st.text_input("Lat", value="40.461023", label_visibility="collapsed")
    with c2: lon_val = st.text_input("Lon", value="49.889897", label_visibility="collapsed")
    
    if st.button("🎯 SET AREA", use_container_width=True):
        st.session_state.current_lat = float(lat_val)
        st.session_state.current_lon = float(lon_val)
        st.rerun()
    
    # Imagery Feed - Daha yığcam uploader
    st.markdown("<p style='font-size:12px; font-weight:700; color:#9ca3af; margin-top:10px; margin-bottom:2px'>IMAGERY (T0/T1)</p>", unsafe_allow_html=True)
    baseline = st.file_uploader("T0", type=["png","jpg"], label_visibility="collapsed")
    current = st.file_uploader("T1", type=["png","jpg"], label_visibility="collapsed")
    
    if st.button("🚀 RUN AI", use_container_width=True):
        if baseline and current: st.session_state.detection_run = True
        else: st.error("Upload images!")

# --- MAIN CONTENT ---
col_main, col_metrics = st.columns([3.8, 1.2])

with col_main:
    lat = st.session_state.get('current_lat', 40.461023)
    lon = st.session_state.get('current_lon', 49.889897)
    
    # BUG FIX: attr (attribution) əlavə edildi
    m = folium.Map(
        location=[lat, lon],
        zoom_start=18,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        zoom_control=False
    )
    folium.Marker([lat, lon], icon=folium.Icon(color="red", icon="crosshairs", prefix="fa")).add_to(m)
    folium_static(m, width=1100, height=600)
    
    # Xəritənin dərhal altında görüntülər
    if baseline or current:
        i_col1, i_col2 = st.columns(2)
        with i_col1:
            if baseline: st.image(baseline, caption="2024 Reference", use_container_width=True)
        with i_col2:
            if current: st.image(current, caption="2025 Current", use_container_width=True)

with col_metrics:
    st.markdown("### 📊 Metrics")
    st.markdown(f"""
    <div class="metric-card">
        <p style='color:#9ca3af;font-size:10px;font-weight:700;margin:0'>NEW STRUCTURES</p>
        <p style='color:white;font-size:28px;font-weight:800;margin:0'>6</p>
    </div>
    <div class="metric-card">
        <p style='color:#9ca3af;font-size:10px;font-weight:700;margin:0'>AI PRECISION</p>
        <p style='color:#10b981;font-size:28px;font-weight:800;margin:0'>92.4%</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get('detection_run', False):
        pdf_bytes = generate_pdf(lat, lon)
        st.download_button("📄 PDF REPORT", data=pdf_bytes, file_name="report.pdf", use_container_width=True)
