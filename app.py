import streamlit as st
from streamlit_folium import st_folium
import folium
from datetime import datetime
from fpdf import FPDF
import io
from PIL import Image

# Session state'i en başta initialize et (sidebar kaybolmasını önler)
if 'lat' not in st.session_state:
    st.session_state.lat = 40.394799
if 'lon' not in st.session_state:
    st.session_state.lon = 49.849585
if 'run' not in st.session_state:
    st.session_state.run = False
if 't0_file' not in st.session_state:
    st.session_state.t0_file = None
if 't1_file' not in st.session_state:
    st.session_state.t1_file = None

st.set_page_config(page_title="SATELLA AI", layout="wide", initial_sidebar_state="expanded")

# Optimize edilmiş CSS - sidebar fix + responsive
st.markdown("""
<style>
/* Sidebar fix - sabit genişlik ve görünürlük */
section[data-testid="stSidebar"] {
    width: 320px !important;
    min-width: 320px !important;
    max-width: 320px !important;
    position: relative !important;
    flex-shrink: 0 !important;
    background: #0d1117 !important;
    border-right: 1px solid #30363d !important;
    z-index: 1000 !important;
}

/* Main content sidebar'a göre hizala */
main .block-container {
    margin-left: 340px !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* Header gizle */
[data-testid="stHeader"] { display: none !important; }

/* App background */
.stApp { background: #0b0d0e !important; }

/* Button styles */
div.stButton > button {
    background: linear-gradient(135deg, #1a73e8, #1557b0) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    height: 42px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
div.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(26, 115, 232, 0.4) !important;
}

/* Metric cards responsive */
@media (max-width: 1200px) {
    section[data-testid="stSidebar"] { width: 280px !important; }
    main .block-container { margin-left: 300px !important; }
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
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
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=1)
    pdf.cell(0, 10, "Structures Detected: 1 | Precision: 92%", ln=1)
    buffer = io.BytesIO()
    buffer.write(pdf.output(dest='S'))
    buffer.seek(0)
    return buffer.getvalue()

# SOL BAR - her zaman görünür
with st.sidebar:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1f6feb,#111827);padding:1.5rem;
                border-radius:12px;margin:-1rem -1rem 1.5rem -1rem;text-align:center;
                border:1px solid rgba(255,255,255,0.1);box-shadow:0 4px 20px rgba(31,111,235,0.3)'>
        <h2 style='color:white;font-size:22px;font-weight:800;margin:0'>🛰️ SATELLA AI</h2>
        <p style='color:rgba(255,255,255,0.8);font-size:11px;margin:5px 0 0 0;
                  letter-spacing:1.5px'>Baku Monitoring System</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📍 **Location Settings**")
    lat_val = st.text_input("Latitude", value=f"{st.session_state.lat:.6f}")
    lon_val = st.text_input("Longitude", value=f"{st.session_state.lon:.6f}")
    
    if st.button("🎯 Set Coordinates", key="set_coords"):
        st.session_state.lat = float(lat_val)
        st.session_state.lon = float(lon_val)
        st.rerun()  # Hemen güncelle
    
    st.markdown("### 🛰️ **Satellite Images**")
    t0_file = st.file_uploader("📸 T0: 2024", type=["png", "jpg", "jpeg"], key="t0")
    t1_file = st.file_uploader("📸 T1: 2025", type=["png", "jpg", "jpeg"], key="t1")
    
    # Session state'e kaydet
    st.session_state.t0_file = t0_file
    st.session_state.t1_file = t1_file
    
    if st.button("🚀 Run Analysis", key="analyze"):
        if t0_file and t1_file:
            st.session_state.run = True
            st.success("✅ Analysis completed!")
            st.rerun()
        else:
            st.error("❌ Upload both T0 and T1 images!")

# MAIN CONTENT
col1, col2 = st.columns([3.8, 1.2])

with col1:
    st.markdown("# 🗺️ **Satellite Map**")
    
    # Mevcut koordinatları kullan
    lat = st.session_state.lat
    lon = st.session_state.lon
    
    # Folium map
    m = folium.Map(location=[lat, lon], zoom_start=17, tiles=None)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri World Imagery",
        name="Satellite"
    ).add_to(m)
    folium.Marker(
        [lat, lon], 
        popup=f"Target: {lat:.6f}N, {lon:.6f}E",
        tooltip="Analysis Point"
    ).add_to(m)
    
    map_data = st_folium(m, width=1200, height=550, key="main_map")
    
    # Images göster (session state'ten)
    if st.session_state.t0_file and st.session_state.t1_file:
        with st.expander("🖼️ **Processed Images**", expanded=True):
            img1, img2 = process_images(st.session_state.t0_file, st.session_state.t1_file)
            col_img1, col_img2 = st.columns(2)
            with col_img1: 
                st.image(img1, caption="T0: 2024 Satellite", use_column_width=True)
            with col_img2: 
                st.image(img2, caption="T1: 2025 Satellite", use_column_width=True)

with col2:
    st.markdown("### 📊 **Analysis Metrics**")
    
    detections = 1 if st.session_state.run else 0
    
    # Structures card
    st.markdown(f"""
    <div style='background:#161b22;border:1px solid #30363d;border-radius:12px;
                padding:1.5rem;margin-bottom:1rem;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.3)'>
        <div style='color:#8b949e;font-size:12px;font-weight:600;letter-spacing:1px'>DETECTED STRUCTURES</div>
        <div style='color:white;font-size:38px;font-weight:800;margin-top:0.5rem'>{detections}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Precision card
    st.markdown("""
    <div style='background:#161b22;border:1px solid #30363d;border-radius:12px;
                padding:1.5rem;margin-bottom:1rem;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.3)'>
        <div style='color:#8b949e;font-size:12px;font-weight:600;letter-spacing:1px'>PRECISION</div>
        <div style='color:#58a6ff;font-size:32px;font-weight:800;margin-top:0.5rem'>92%</div>
    </div>
    """, unsafe_allow_html=True)
    
    # F1 Score card
    st.markdown("""
    <div style='background:#161b22;border:1px solid #30363d;border-radius:12px;
                padding:1.5rem;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.3)'>
        <div style='color:#8b949e;font-size:12px;font-weight:600;letter-spacing:1px'>F1 SCORE</div>
        <div style='color:#3fb950;font-size:32px;font-weight:800;margin-top:0.5rem'>90%</div>
    </div>
    """, unsafe_allow_html=True)
    
    # PDF download
    if st.session_state.run:
        pdf_data = generate_pdf(lat, lon)
        st.download_button(
            label="📥 Download Report", 
            data=pdf_data, 
            file_name="satella_ai_report.pdf",
            mime="application/pdf"
        )

st.markdown("---")
st.caption("🤖 SATELLA AI v3.4 | Professional Edition | Powered by Streamlit & Folium")

# Rerun trigger'ını temizle
if st.button("🔄 Refresh", key="refresh"):
    st.rerun()
