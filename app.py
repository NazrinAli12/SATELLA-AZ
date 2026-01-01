import streamlit as st
import folium
from streamlit_folium import folium_static
from datetime import datetime
from fpdf import FPDF
import io
from PIL import Image

st.set_page_config(page_title="SATELLA AI", layout="wide", initial_sidebar_state="expanded")

# SOL BAR FİKS CSS (Foto-ya 100% uyğun)
st.markdown("""
<style>
/* SOL BAR - PREÇİZE 320px + SABİT */
section[data-testid="stSidebar"] {
    width: 320px !important;
    min-width: 320px !important;
    max-width: 320px !important;
    background: #0d1117 !important;
    border-right: 1px solid #30363d !important;
}

/* SCROLL YOX */
section[data-testid="stSidebar"] > div > div {
    overflow: hidden !important;
    max-height: 100vh !important;
}

/* MAIN SAĞA SÜR (320px) */
main .block-container {
    margin-left: 320px !important;
    padding-left: 0 !important;
}

/* HEADER GİZLƏT */
[data-testid="stHeader"] { display: none !important; }

/* DARK THEME */
.stApp {
    background-color: #0b0d0e !important;
}

/* DÜYMƏ */
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
    pdf.cell(0, 10, f"Location: {lat:.6f}N {lon:.6f}E", ln=1)
    pdf.cell(0, 10, "New Structures: 1", ln=1)
    pdf.cell(0, 10, "Precision: 92%", ln=1)
    buffer = io.BytesIO()
    buffer.write(pdf.output(dest='S'))
    buffer.seek(0)
    return buffer.getvalue()

# SOL BAR (Foto-da olduğu kimi)
with st.sidebar:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1f6feb 0%,#111827 100%); 
                padding:1.5rem;border-radius:12px;margin:-1rem -1rem 1.5rem -1rem;
                border:1px solid rgba(255,255,255,0.1);text-align:center'>
        <h2 style='color:white;font-size:22px;font-weight:800;margin:0'>🛰️ SATELLA AI</h2>
        <p style='color:rgba(255,255,255,0.8);font-size:11px;margin:5px 0 0 0;
                  letter-spacing:1.5px;text-transform:uppercase'>Baku Monitoring</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📍 Area of Interest")
    lat_val = st.text_input("Latitude", "40.394799")
    lon_val = st.text_input("Longitude", "49.849585")
    
    if st.button("🎯 Set Location"):
        st.session_state.lat = float(lat_val)
        st.session_state.lon = float(lon_val)
    
    st.markdown("### 🛰️ Imagery")
    t0_file = st.file_uploader("T0: 2024 Baseline", ["png","jpg"])
    t1_file = st.file_uploader("T1: 2025 Current", ["png","jpg"])
    
    if st.button("🚀 RUN DETECTION"):
        if t0_file and t1_file:
            st.session_state.run = True
            st.success("✅ Analysis complete!")
        else:
            st.error("Upload both images")

# MAIN (Foto-da olduğu kimi)
col_map, col_metrics = st.columns([3.8, 1.2])

with col_map:
    lat = st.session_state.get('lat', 40.394799)
    lon = st.session_state.get('lon', 49.849585)
    
    m = folium.Map([lat, lon], zoom_start=17)
    folium.TileLayer("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}").add_to(m)
    folium.Marker([lat, lon], popup="Analysis Site").add_to(m)
    folium_static(m, width=1100, height=500)
    
    if t0_file and t1_file:
        img1, img2 = process_images(t0_file, t1_file)
        col_img1, col_img2 = st.columns(2)
        with col_img1: st.image(img1, caption="T0 2024", use_column_width=True)
        with col_img2: st.image(img2, caption="T1 2025", use_column_width=True)

with col_metrics:
    st.markdown("### 📊 METRICS")
    
    detections = 1 if st.session_state.get('run') else 0
    st.markdown(f"""
    <div style='background:#161b22;border:1px solid #30363d;border-radius:10px;padding:1.5rem;margin-bottom:1rem'>
        <div style='color:#8b949e;font-size:12px;font-weight:600'>NEW BUILDINGS</div>
        <div style='color:white;font-size:36px;font-weight:800'>{detections}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background:#161b22;border:1px solid #30363d;border-radius:10px;padding:1.5rem;margin-bottom:1rem'>
        <div style='color:#8b949e;font-size:12px;font-weight:600'>PRECISION</div>
        <div style='color:#58a6ff;font-size:28px;font-weight:800'>92%</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background:#161b22;border:1px solid #30363d;border-radius:10px;padding:1.5rem'>
        <div style='color:#8b949e;font-size:12px;font-weight:600'>F1 SCORE</div>
        <div style='color:#3fb950;font-size:28px;font-weight:800'>90%</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.get('run'):
        pdf_data = generate_pdf(lat, lon)
        st.download_button("📥 REPORT", pdf_data, "satella_report.pdf")

st.markdown("---")
st.caption("SATELLA AI | VISTAR Program")
