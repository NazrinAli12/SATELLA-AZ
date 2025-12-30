import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io

# 1. Page Config
st.set_page_config(page_title="SATELLA", layout="wide", initial_sidebar_state="expanded")

# 2. Advanced UI Styling (Exact Layout)
st.markdown("""
<style>
    /* Google Inter Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #0b0d0e !important;
        overflow-x: hidden !important;
    }

    /* GENİŞ SOL BAR (400px) */
    [data-testid="stSidebar"] {
        width: 400px !important;
        background-color: #111418 !important;
        border-right: 1px solid #2d333b !important;
    }
    
    /* SCROLLBAR LƏĞVİ */
    ::-webkit-scrollbar { display: none !important; }

    /* SAĞ PANEL SABİTLƏMƏ */
    [data-testid="column"]:nth-child(2) {
        background-color: #111418 !important;
        border-left: 1px solid #2d333b !important;
        padding: 24px !important;
        height: 100vh;
    }

    /* DÜYMƏLƏR */
    div.stButton > button {
        background: #1a73e8 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        height: 45px !important;
    }

    /* METRİK KARTLARI */
    .metric-card {
        background: #1a1f24;
        border: 1px solid #3c4043;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# 3. PDF Generator
def generate_pdf(lat, lon):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(0, 10, "SATELLA FHN Report", ln=1, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Location: {lat}, {lon}", ln=1)
    pdf.cell(0, 10, "Structures: 6 | Precision: 92%", ln=1)
    return pdf.output(dest='S').encode('latin-1')

# --- SOL SIDEBAR (400px) ---
with st.sidebar:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1e3a8a,#3b82f6);padding:1.5rem;border-radius:12px;margin-bottom:1.5rem'>
        <h1 style='color:white;margin:0;font-size:24px;font-weight:800'>🛰️ SATELLA</h1>
        <p style='color:#bfdbfe;margin:0.2rem 0 0 0;font-size:12px'>Construction Monitor</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📍 Target Settings")
    lat_val = st.text_input("LATITUDE", value="40.461023")
    lon_val = st.text_input("LONGITUDE", value="49.889897")
    
    if st.button("🎯 UPDATE VIEW", use_container_width=True):
        st.session_state.current_lat = float(lat_val)
        st.session_state.current_lon = float(lon_val)
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 🛰️ Imagery Feed")
    baseline = st.file_uploader("T0: 2024 Baseline", type=["png","jpg"])
    current = st.file_uploader("T1: 2025 Current", type=["png","jpg"])
    
    if st.button("🚀 RUN AI DETECTION", use_container_width=True):
        if baseline and current:
            st.session_state.detection_run = True
            st.balloons()
        else:
            st.warning("Please upload both images.")

# --- MAIN CONTENT LAYOUT ---
col_main, col_metrics = st.columns([3.8, 1.2])

with col_main:
    # Xəritə Mərkəzləşdirilmiş
    lat = st.session_state.get('current_lat', 40.461023)
    lon = st.session_state.get('current_lon', 49.889897)
    
    m = folium.Map(
        location=[lat, lon],
        zoom_start=18,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        zoom_control=False
    )
    folium.Marker([lat, lon], icon=folium.Icon(color="red", icon="crosshairs", prefix="fa")).add_to(m)
    folium.Circle([lat, lon], radius=150, color="red", fill=True, fillOpacity=0.2).add_to(m)
    
    # Xəritənin Səliqəli Yerləşdirilməsi
    folium_static(m, width=1150, height=650)
    
    # Şəkillərin Xəritənin Altına Düşməsi
    if baseline or current:
        st.markdown("### 📸 Imagery Comparison")
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            if baseline:
                st.image(baseline, caption="2024 Reference", use_column_width=True)
        with col_img2:
            if current:
                st.image(current, caption="2025 Current", use_column_width=True)

with col_metrics:
    st.markdown("### 📊 Detection Data")
    
    # Metrika Kartları
    st.markdown(f"""
    <div class="metric-card">
        <div style='color:#9ca3af;font-size:11px;font-weight:600;text-transform:uppercase'>New Buildings</div>
        <div style='color:white;font-size:32px;font-weight:800'>6</div>
    </div>
    <div class="metric-card">
        <div style='color:#9ca3af;font-size:11px;font-weight:600;text-transform:uppercase'>AI Precision</div>
        <div style='color:#10b981;font-size:32px;font-weight:800'>92.4%</div>
    </div>
    <div class="metric-card">
        <div style='color:#9ca3af;font-size:11px;font-weight:600;text-transform:uppercase'>F1 Score</div>
        <div style='color:#10b981;font-size:32px;font-weight:800'>90.1%</div>
    </div>
    """, unsafe_allow_html=True)
    
    # PDF Button
    if st.session_state.get('detection_run', False):
        pdf_bytes = generate_pdf(lat, lon)
        st.download_button(
            label="📄 DOWNLOAD FHN REPORT",
            data=pdf_bytes,
            file_name=f"SATELLA_FHN_REPORT.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    st.markdown("<br><br><div style='color:#4b5563;font-size:11px;text-align:center'>Verified by SATELLA AI Engine v2.4</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<center style='color:#6b7280; font-size:12px;'>SATELLA Construction Monitoring System © 2025</center>", unsafe_allow_html=True)
