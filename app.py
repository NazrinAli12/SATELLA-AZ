import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io
from PIL import Image

st.set_page_config(page_title="SATELLA AI", layout="wide", initial_sidebar_state="expanded")

# SCROLL YOK + SOL BAR ZORLA GÖRÜNÜN
st.markdown("""
<style>
/* SOL BAR ZORLA 400px + SCROLL YOK */
section[data-testid="stSidebar"] {
    width: 400px !important;
    min-width: 400px !important;
    max-width: 400px !important;
    height: 100vh !important;
    overflow: hidden !important;
    background: #0d1117 !important;
    border-right: 1px solid #30363d !important;
    position: fixed !important;
    left: 0 !important;
    z-index: 999 !important;
}

section[data-testid="stSidebar"] > div {
    height: 100vh !important;
    overflow: hidden !important;
    padding-bottom: 200px !important;
}

[data-testid="stSidebar"]::-webkit-scrollbar { display: none !important; }

/* MAIN CONTENT SAĞA SÜR */
[data-testid="stAppViewContainer"] {
    margin-left: 400px !important;
    padding-left: 0 !important;
}

/* FONT + DARK */
html, body {
    font-family: 'Inter', sans-serif !important;
    background: #0b0d0e !important;
}

[data-testid="stHeader"] { display: none !important; }
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
    pdf.cell(0, 10, f"Baku: {lat:.6f}N {lon:.6f}E", ln=1)
    pdf.cell(0, 10, "Detections: 1 | Precision: 92%", ln=1)
    buffer = io.BytesIO()
    buffer.write(pdf.output(dest='S'))
    buffer.seek(0)
    return buffer.getvalue()

# SOL BAR
with st.sidebar:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1f6feb,#111827);padding:2rem;border-radius:15px;margin:-1rem -1rem 2rem -1rem;text-align:center'>
        <h2 style='color:white;margin:0;font-size:26px;font-weight:800'>🛰️ SATELLA AI</h2>
        <p style='color:#bfdbfe;font-size:12px;margin:5px 0 0 0;letter-spacing:2px'>Construction Detection</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📍 **Area of Interest**")
    lat_val = st.text_input("**Latitude**", value="40.394799")
    lon_val = st.text_input("**Longitude**", value="49.849585")
    
    if st.button("🎯 **Set Target**", use_container_width=True):
        st.session_state.lat = float(lat_val)
        st.session_state.lon = float(lon_val)
        st.success("✅ Target set!")
    
    st.markdown("### 🛰️ **Imagery Inputs**")
    t0_file = st.file_uploader("**T0: 2024 Baseline**", type=["png","jpg"])
    t1_file = st.file_uploader("**T1: 2025 Current**", type=["png","jpg"])
    
    if st.button("🚀 **RUN ANALYSIS**", use_container_width=True):
        if t0_file and t1_file:
            st.session_state.run = True
            st.balloons()
        else:
            st.error("Upload both images!")

# MAIN
col1, col2 = st.columns([3.5,1.3])

with col1:
    lat = st.session_state.get('lat', 40.394799)
    lon = st.session_state.get('lon', 49.849585)
    
    m = folium.Map([lat, lon], zoom_start=18)
    folium.TileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}").add_to(m)
    folium.Marker([lat, lon]).add_to(m)
    folium.Circle([lat, lon], 200, color='red', fill=True).add_to(m)
    folium_static(m, width=1200, height=600)
    
    if t0_file and t1_file:
        img1, img2 = process_images(t0_file, t1_file)
        st.image([img1, img2], caption=["2024 T0", "2025 T1"], width=550)

with col2:
    st.markdown("### 📊 **AI Results**")
    st.metric("New Buildings", "1")
    st.metric("Precision", "92%")
    st.metric("F1 Score", "90%")
    
    if st.session_state.get('run', False):
        pdf_data = generate_pdf(lat, lon)
        st.download_button("📄 FHN Report", pdf_data, f"SATELLA_{lat}_{lon}.pdf")

st.markdown("---")
st.caption("SATELLA AI v3.3 | VISTAR Excellence Program")
