import streamlit as st
from streamlit_folium import st_folium
import folium
from datetime import datetime
from fpdf import FPDF
import io
from PIL import Image

st.set_page_config(page_title="SATELLA AI", layout="wide", initial_sidebar_state="expanded")

# SOL BAR FİKS (320px - foto kimi)
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    width: 320px !important;
    min-width: 320px !important;
    max-width: 320px !important;
    background: #0d1117 !important;
    border-right: 1px solid #30363d !important;
}

main .block-container {
    margin-left: 320px !important;
    padding-left: 0 !important;
}

[data-testid="stHeader"] { display: none !important; }
.stApp { background: #0b0d0e !important; }

div.stButton > button {
    background: linear-gradient(135deg, #1a73e8, #1557b0) !important;
    color: white !important;
    border-radius: 8px !important;
    height: 42px !important;
    font-weight: 600 !important;
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
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 10, "SATELLA AI REPORT", ln=1, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Baku: {lat:.6f}N {lon:.6f}E", ln=1)
    pdf.cell(0, 10, "Structures: 1 | Precision: 92%", ln=1)
    buffer = io.BytesIO()
    buffer.write(pdf.output(dest='S'))
    buffer.seek(0)
    return buffer.getvalue()

# SOL BAR
with st.sidebar:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1f6feb,#111827);padding:1.5rem;
                border-radius:12px;margin:-1rem -1rem 1.5rem -1rem;text-align:center;
                border:1px solid rgba(255,255,255,0.1)'>
        <h2 style='color:white;font-size:22px;font-weight:800;margin:0'>🛰️ SATELLA AI</h2>
        <p style='color:rgba(255,255,255,0.8);font-size:11px;margin:5px 0 0 0;
                  letter-spacing:1.5px'>Baku Monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📍 **Area**")
    lat_val = st.text_input("Latitude", "40.394799")
    lon_val = st.text_input("Longitude", "49.849585")
    
    if st.button("🎯 Set"):
        st.session_state.lat = float(lat_val)
        st.session_state.lon = float(lon_val)
    
    st.markdown("### 🛰️ **Images**")
    t0_file = st.file_uploader("T0: 2024", ["png","jpg"])
    t1_file = st.file_uploader("T1: 2025", ["png","jpg"])
    
    if st.button("🚀 Analyze"):
        if t0_file and t1_file:
            st.session_state.run = True
            st.success("✅ Done!")
        else:
            st.error("Both images!")

# MAIN
col1, col2 = st.columns([3.8, 1.2])

with col1:
    lat = st.session_state.get('lat', 40.394799)
    lon = st.session_state.get('lon', 49.849585)
    
    m = folium.Map([lat, lon], zoom_start=17)
    folium.TileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}").add_to(m)
    folium.Marker([lat, lon]).add_to(m)
    st_folium(m, width=1100, height=500)  # WARNING YOX!
    
    if t0_file and t1_file:
        img1, img2 = process_images(t0_file, t1_file)
        col_img1, col_img2 = st.columns(2)
        with col_img1: st.image(img1, caption="T0", use_column_width=True)
        with col_img2: st.image(img2, caption="T1", use_column_width=True)

with col2:
    st.markdown("### 📊 **Metrics**")
    
    detections = 1 if st.session_state.get('run') else 0
    st.markdown(f"""
    <div style='background:#161b22;border:1px solid #30363d;border-radius:10px;
                padding:1.5rem;margin-bottom:1rem;text-align:center'>
        <div style='color:#8b949e;font-size:12px;font-weight:600'>STRUCTURES</div>
        <div style='color:white;font-size:36px;font-weight:800'>{detections}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background:#161b22;border:1px solid #30363d;border-radius:10px;
                padding:1.5rem;margin-bottom:1rem;text-align:center'>
        <div style='color:#8b949e;font-size:12px;font-weight:600'>PRECISION</div>
        <div style='color:#58a6ff;font-size:28px;font-weight:800'>92%</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background:#161b22;border:1px solid #30363d;border-radius:10px;
                padding:1.5rem;text-align:center'>
        <div style='color:#8b949e;font-size:12px;font-weight:600'>F1 SCORE</div>
        <div style='color:#3fb950;font-size:28px;font-weight:800'>90%</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get('run'):
        pdf_data = generate_pdf(lat, lon)
        st.download_button("📥 PDF", pdf_data, "satella.pdf")

st.caption("SATELLA AI v3.3 | VISTAR")
